import os  # 导入操作系统路径工具
import struct  # 导入二进制结构解析工具
import unittest  # 导入单元测试框架
from datetime import datetime  # 导入日期时间类型

from main import (  # 导入待测试的主模块功能
    bolden_coverage,
    clamp_position,
    format_time,
    is_hex_color,
    make_startup_command,
    MovementController,
    migrate_legacy_transparency,
    point_inside_bounds,
    render_clock_bgra,
    shortcut_for_key,
    supports_dwm_rounded_corners,
    tray_menu_position,
    transparency_to_alpha,
)


class FormatTimeTests(unittest.TestCase):  # 测试时间格式化
    def test_formats_morning_time(self) -> None:  # 测试上午时间
        self.assertEqual(format_time(datetime(2024, 1, 1, 9, 5)), "09:05 AM")  # 校验上午格式

    def test_formats_noon_and_midnight(self) -> None:  # 测试正午和午夜
        self.assertEqual(format_time(datetime(2024, 1, 1, 12, 0)), "12:00 PM")  # 校验正午格式
        self.assertEqual(format_time(datetime(2024, 1, 1, 0, 0)), "12:00 AM")  # 校验午夜格式


class ClockTextRenderingTests(unittest.TestCase):  # 测试时钟文本渲染
    def test_text_coverage_is_boosted_slightly_without_clipping(self) -> None:  # 测试覆盖度增强
        self.assertEqual(bolden_coverage(0), 0)  # 校验最小覆盖度
        self.assertEqual(bolden_coverage(128), 138)  # 校验中间覆盖度
        self.assertEqual(bolden_coverage(255), 255)  # 校验最大覆盖度

    def test_white_text_uses_premultiplied_per_pixel_alpha(self) -> None:  # 测试白字逐像素预乘 alpha
        width, height, pixels = render_clock_bgra(  # 渲染白色时钟图像
            "12:24 PM", 32, "#FFFFFF", 96
        )
        self.assertEqual(len(pixels), width * height * 4)  # 校验像素缓冲区长度
        alphas = pixels[3::4]  # 提取 alpha 通道
        self.assertEqual(pixels[:4], b"\x00\x00\x00\x00")  # 校验首像素为透明
        self.assertIn(255, alphas)  # 确信存在不透明像素
        self.assertTrue(any(0 < alpha < 255 for alpha in alphas))  # 确信存在半透明像素
        for index in range(0, len(pixels), 4):  # 遍历每个 BGRA 像素
            blue, green, red, alpha = pixels[index : index + 4]  # 分离通道值
            self.assertEqual((blue, green, red), (alpha, alpha, alpha))  # 校验白色通道预乘结果

    def test_color_channels_are_premultiplied_by_coverage(self) -> None:  # 测试彩色通道预乘
        width, height, pixels = render_clock_bgra(  # 渲染红色时钟图像
            "12:24 PM", 32, "#FF0000", 96
        )
        self.assertEqual(len(pixels), width * height * 4)  # 校验像素缓冲区长度
        self.assertTrue(  # 校验红色通道与 alpha 的关系
            all(
                pixels[index] == pixels[index + 1] == 0
                and pixels[index + 2] == pixels[index + 3]
                for index in range(0, len(pixels), 4)
            )
        )


class ClampPositionTests(unittest.TestCase):  # 测试位置限制
    def test_clamps_to_virtual_desktop_edges(self) -> None:  # 测试虚拟桌面边缘
        bounds = (-1920, 0, 3840, 1080)  # 设置虚拟桌面边界
        self.assertEqual(  # 校验左上角越界限制
            clamp_position(-5000, -500, 200, 100, bounds),
            (-1920, 0),
        )
        self.assertEqual(  # 校验右下角越界限制
            clamp_position(5000, 5000, 200, 100, bounds),
            (1720, 980),
        )


class PointBoundsTests(unittest.TestCase):  # 测试点是否在边界内
    def test_menu_bounds_include_top_left_but_exclude_bottom_right(self) -> None:  # 测试半开区间边界
        bounds = (100, 200, 300, 400)  # 设置矩形边界
        self.assertTrue(point_inside_bounds(100, 200, bounds))  # 左上角应包含
        self.assertTrue(point_inside_bounds(299, 399, bounds))  # 内部点应包含
        self.assertFalse(point_inside_bounds(99, 200, bounds))  # 左侧外部点应排除
        self.assertFalse(point_inside_bounds(300, 200, bounds))  # 右侧边界应排除
        self.assertFalse(point_inside_bounds(100, 400, bounds))  # 底部边界应排除


class TrayMenuPositionTests(unittest.TestCase):  # 测试托盘菜单位置
    def test_menu_is_shifted_up_even_when_screen_edge_clamps_it(self) -> None:  # 测试向上偏移和边缘限制
        bounds = (0, 0, 350, 557)  # 设置窄屏边界
        self.assertEqual(  # 校验菜单位置
            tray_menu_position(325, 530, 166, 502, bounds),
            (184, 40),
        )

    def test_menu_position_stays_within_screen_bounds(self) -> None:  # 测试菜单保持在屏幕内
        bounds = (0, 0, 1920, 1080)  # 设置全屏边界
        x, y = tray_menu_position(100, 100, 166, 502, bounds)  # 计算菜单坐标
        self.assertEqual((x, y), (104, 62))  # 校验计算结果


class ShortcutTests(unittest.TestCase):  # 测试快捷键处理
    def test_ctrl_arrow_moves_without_reserving_the_shortcut(self) -> None:  # 测试方向快捷键
        self.assertEqual(shortcut_for_key(0x25, True, False), "left")  # 校验向左
        self.assertEqual(shortcut_for_key(0x28, True, False), "down")  # 校验向下

    def test_other_keys_do_not_trigger_shortcuts(self) -> None:  # 测试无关按键
        self.assertIsNone(shortcut_for_key(0x25, False, False))  # 未按 Ctrl 不触发
        self.assertIsNone(shortcut_for_key(0x51, True, False))  # 普通字母不触发
        self.assertEqual(shortcut_for_key(0x51, True, True), "quit")  # 按 Q 加修饰键退出


class StartupCommandTests(unittest.TestCase):  # 测试启动命令
    def test_uses_pythonw_and_quotes_paths_with_spaces(self) -> None:  # 测试含空格路径
        command = make_startup_command(  # 生成启动命令
            r"C:\Program Files\Python\python.exe",
            r"E:\Time Overlay\main.py",
        )
        self.assertEqual(  # 校验命令格式
            command,
            r'"C:\Program Files\Python\pythonw.exe" "E:\Time Overlay\main.py"',
        )


class ClockIconTests(unittest.TestCase):  # 测试时钟托盘图标
    def test_tray_icon_contains_multiple_resolution_frames(self) -> None:  # 测试多尺寸图标帧
        icon_path = os.path.join(os.path.dirname(__file__), "tray_icon.ico")  # 定位图标文件
        with open(icon_path, "rb") as icon_file:  # 以二进制打开图标
            data = icon_file.read()  # 读取图标字节
        reserved, icon_type, count = struct.unpack_from("<HHH", data)  # 解包图标头
        self.assertEqual((reserved, icon_type), (0, 1))  # 校验 ICO 头
        self.assertGreaterEqual(count, 3)  # 确信至少三帧
        entries = [  # 解包每个图像目录项
            struct.unpack_from("<BBBBHHII", data, 6 + index * 16)
            for index in range(count)
        ]
        sizes = {(width or 256, height or 256) for width, height, *_ in entries}  # 收集图像尺寸
        self.assertTrue({(16, 16), (32, 32), (48, 48)}.issubset(sizes))  # 校验所需尺寸
        _, _, _, _, _, _, byte_count, offset = next(  # 获取 32 像素帧位置
            entry for entry in entries if entry[0] == 32
        )
        self.assertLessEqual(offset + byte_count, len(data))  # 校验帧数据边界

        dib_header_size = struct.unpack_from("<I", data, offset)[0]  # 获取 DIB 头长度
        self.assertEqual(dib_header_size, 40)  # 校验常规 DIB 头
        pixel_offset = offset + dib_header_size  # 计算像素起始位置

        def pixel_alpha(x: int, y: int) -> int:  # 定义像素 alpha 读取器
            row_from_bottom = 31 - y  # 将顶部坐标转为底部行号
            index = pixel_offset + (row_from_bottom * 32 + x) * 4 + 3  # 计算 alpha 字节偏移
            return data[index]  # 返回 alpha 值

        self.assertEqual(pixel_alpha(0, 0), 0)  # 左上角应透明
        self.assertGreater(pixel_alpha(16, 16), 0)  # 中心应不透明


class ColorSettingTests(unittest.TestCase):  # 测试颜色设置
    def test_accepts_hex_colors_and_rejects_other_values(self) -> None:  # 测试十六进制颜色校验
        self.assertTrue(is_hex_color("#12aBcF"))  # 合法大小写混合格式应接受
        self.assertFalse(is_hex_color("#12345"))  # 缺少一位应拒绝
        self.assertFalse(is_hex_color("white"))  # 名称格式应拒绝
        self.assertFalse(is_hex_color("#12345g"))  # 非十六进制字符应拒绝


class TransparencySettingTests(unittest.TestCase):  # 测试透明度设置
    def test_transparency_maps_to_semitransparent_alpha(self) -> None:  # 测试透明度映射
        from main import (  # 导入透明度常量
            DEFAULT_TRANSPARENCY,
            MAX_TRANSPARENCY,
            MIN_TRANSPARENCY,
        )

        self.assertEqual(DEFAULT_TRANSPARENCY, 43)  # 校验默认透明度
        self.assertEqual((MIN_TRANSPARENCY, MAX_TRANSPARENCY), (10, 70))  # 校验透明度范围
        self.assertEqual(transparency_to_alpha(20), 204)  # 校验低透明度映射
        self.assertEqual(transparency_to_alpha(35), 166)  # 校验中透明度映射
        self.assertEqual(transparency_to_alpha(50), 128)  # 校验半透明映射
        with self.assertRaises(ValueError):  # 校验越界异常
            transparency_to_alpha(71)  # 超出范围应抛出异常

    def test_legacy_slider_value_migrates_to_semitransparent_range(self) -> None:  # 测试旧滑块迁移
        self.assertEqual(migrate_legacy_transparency(20), 10)  # 校验低端迁移
        self.assertEqual(migrate_legacy_transparency(82), 56)  # 校验中间迁移
        self.assertEqual(migrate_legacy_transparency(100), 70)  # 校验高端迁移
        with self.assertRaises(ValueError):  # 校验越界异常
            migrate_legacy_transparency(101)  # 超出范围应抛出异常


class RoundedCornerCompatibilityTests(unittest.TestCase):  # 测试圆角兼容性
    def test_dwm_rounded_corners_are_only_used_on_windows_11(self) -> None:  # 测试仅在 Windows 11 启用
        self.assertFalse(supports_dwm_rounded_corners(19045))  # 旧版 Windows 应禁用
        self.assertFalse(supports_dwm_rounded_corners(21999))  # Windows 10 构建应禁用
        self.assertTrue(supports_dwm_rounded_corners(22000))  # Windows 11 构建应启用


class MovementControllerTests(unittest.TestCase):  # 测试移动控制器
    def test_holding_direction_accelerates_and_release_decelerates(self) -> None:  # 测试按住加速和释放减速
        controller = MovementController()  # 创建移动控制器
        controller.set_key("right", True)  # 按下向右键
        first_dx, _ = controller.update(0.016)  # 更新一次并取得初始位移
        for _ in range(30):  # 连续更新加速阶段
            later_dx, _ = controller.update(0.016)  # 记录后续位移
        self.assertGreater(first_dx, 0)  # 初始位移应为正
        self.assertGreater(later_dx, first_dx)  # 加速后位移应更大

        controller.set_key("right", False)  # 释放向右键
        first_release_dx, _ = controller.update(0.016)  # 更新一次并取得释放初位移
        for _ in range(100):  # 连续更新减速阶段
            last_release_dx, _ = controller.update(0.016)  # 记录最终位移
        self.assertGreater(first_release_dx, 0)  # 释放初位移应为正
        self.assertLess(last_release_dx, first_release_dx)  # 减速后位移应更小
        self.assertAlmostEqual(controller.velocity_x, 0)  # 最终速度应趋近于零

    def test_diagonal_motion_is_normalized(self) -> None:  # 测试斜向移动归一化
        horizontal = MovementController()  # 创建水平运动控制器
        horizontal.set_key("right", True)  # 按下水平向右键
        horizontal_dx, horizontal_dy = horizontal.update(0.016)  # 更新水平位移

        diagonal = MovementController()  # 创建斜向运动控制器
        diagonal.set_key("right", True)  # 同时按下向右键
        diagonal.set_key("up", True)  # 同时按下向上键
        diagonal_dx, diagonal_dy = diagonal.update(0.016)  # 更新斜向位移

        self.assertAlmostEqual(diagonal_dx, horizontal_dx / 2**0.5)  # 校验斜向水平分量
        self.assertAlmostEqual(diagonal_dy, -horizontal_dx / 2**0.5)  # 校验斜向垂直分量
        self.assertAlmostEqual(  # 校验合成速度保持不变
            (diagonal_dx**2 + diagonal_dy**2) ** 0.5,
            (horizontal_dx**2 + horizontal_dy**2) ** 0.5,
        )

    def test_opposite_directions_cancel(self) -> None:  # 测试相反方向抵消
        controller = MovementController()  # 创建移动控制器
        controller.set_key("left", True)  # 按下向左键
        controller.set_key("right", True)  # 同时按下向右键
        dx, dy = controller.update(0.016)  # 更新移动位移
        self.assertEqual((dx, dy), (0, 0))  # 相反方向位移应为零


if __name__ == "__main__":  # 作为脚本运行时执行
    unittest.main()
