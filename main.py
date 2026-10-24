import ctypes #调用Windows API
import math #数学函数
import os #文件和路径操作
import queue #队列数据结构
import subprocess #子进程管理
import sys #系统相关操作
import time #时间相关操作
import tkinter as tk #GUI库
from ctypes import wintypes #API
from datetime import datetime #日期
from tkinter import colorchooser, messagebox, simpledialog #GUI对话框


DEFAULT_TRANSPARENCY = 43 #窗口默认透明度
MIN_TRANSPARENCY = 10 #透明度允许范围10-70
MAX_TRANSPARENCY = 70 #透明度允许范围10-70
LEGACY_MIN_TRANSPARENCY = 20 #旧版本透明度允许范围20-100
LEGACY_MAX_TRANSPARENCY = 100 #旧版本透明度允许范围20-100
PERCENT_SCALE = 100 #百分比缩放
TRAY_MENU_EXTRA_UPWARD_OFFSET = 15 #托盘菜单额外向上偏移
FONT_FAMILY = "Segoe UI" #字体家族
MENU_FONT_FAMILY = "Microsoft YaHei UI" #菜单字体家族
MENU_ITEM_FONT_SIZE = 10 #菜单项字体大小
MENU_HEADING_FONT_SIZE = 9 #菜单标题字体大小
FONT_SIZE_PRESETS = (20, 24, 32, 40, 64)#最小12最大95
COLOR_PRESETS = (
    ("白色", "#FFFFFF"),
    ("灰色", "#9E9E9E"),
    ("红色", "#FF5C5C"),
    ("黄色", "#FFD54A"),
    ("绿色", "#4CAF50"),
    ("青色", "#26C6DA"),
    ("蓝色", "#5C6BC0"),
    ("紫色", "#AB47BC"),
)
WM_KEYDOWN = 0x0100 #键盘按下消息 
WM_KEYUP = 0x0101#键盘抬起消息
WM_SYSKEYDOWN = 0x0104#系统键盘按下消息
WM_SYSKEYUP = 0x0105#系统键盘抬起消息
WH_KEYBOARD_LL = 13#低级键盘钩子
WH_MOUSE_LL = 14#低级鼠标钩子
VK_CONTROL = 0x11#Control键
VK_SHIFT = 0x10#Shift键
VK_QUIT = 0x51#Quit键
CTRL_DOWN_MASK = 0x8000#Ctrl键按下掩码
ARROW_KEYS = {0x25: "left", 0x26: "up", 0x27: "right", 0x28: "down"}#方向键

WM_CLOSE = 0x0010#关闭窗口消息
WM_LBUTTONUP = 0x0202#鼠标左键抬起消息
WM_LBUTTONDOWN = 0x0201#鼠标左键按下消息
WM_RBUTTONDOWN = 0x0204#鼠标右键按下消息
WM_MBUTTONDOWN = 0x0207#鼠标中键按下消息
WM_XBUTTONDOWN = 0x020B#鼠标X键按下消息
WM_APP = 0x8000#应用程序自定义消息
TRAY_CALLBACK_MESSAGE = WM_APP + 1#托盘回调消息
NIM_ADD = 0x00000000#托盘图标添加消息
NIM_DELETE = 0x00000002#托盘图标删除消息
NIF_MESSAGE = 0x00000001#托盘图标消息标志
NIF_ICON = 0x00000002#托盘图标图标标志
NIF_TIP = 0x00000004#托盘图标提示标志
AUTOSTART_VALUE_NAME = "ALS-WindowsTimeOverlay"#自启动值名称
SETTINGS_KEY_PATH = r"Software\WindowsTimeOverlay"#设置键路径
SINGLE_INSTANCE_MUTEX_NAME = "Local\\WindowsTimeOverlay_SingleInstance"#单实例互斥体名称
ERROR_ALREADY_EXISTS = 183#错误：已存在
APP_PUBLISHER = "ALS"#应用程序发布者

HOOKPROC = ctypes.WINFUNCTYPE(
    ctypes.c_ssize_t, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM
)
WNDPROC = ctypes.WINFUNCTYPE(
    wintypes.LPARAM,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


class WNDCLASSW(ctypes.Structure):#窗口类结构
    _fields_ = (
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    )


class NOTIFYICONDATAW(ctypes.Structure):   #托盘图标数据结构
    class _TimeoutOrVersion(ctypes.Union):#超时或版本联合体
        _fields_ = (("uTimeout", wintypes.UINT), ("uVersion", wintypes.UINT))

    class _Guid(ctypes.Structure):  # 定义 GUID 结构体，用于标识通知图标
        _fields_ = (  # 定义结构体的字段列表
            ("Data1", wintypes.DWORD),  # GUID 的第 1 个字段，32 位无符号整数
            ("Data2", wintypes.WORD),  # GUID 的第 2 个字段，16 位无符号整数
            ("Data3", wintypes.WORD),  # GUID 的第 3 个字段，16 位无符号整数
            ("Data4", ctypes.c_ubyte * 8),  # GUID 的第 4 个字段，8 个无符号字节
        )

    _anonymous_ = ("timeout_or_version",)
    _fields_ = (
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", wintypes.WCHAR * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", wintypes.WCHAR * 256),
        ("timeout_or_version", _TimeoutOrVersion),
        ("szInfoTitle", wintypes.WCHAR * 64),
        ("dwInfoFlags", wintypes.DWORD),
        ("guidItem", _Guid),
        ("hBalloonIcon", wintypes.HICON),
    )


class POINT(ctypes.Structure):#点结构
    _fields_ = (("x", wintypes.LONG), ("y", wintypes.LONG))


class MSLLHOOKSTRUCT(ctypes.Structure):#低级鼠标钩子结构
    _fields_ = (
        ("pt", POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    )


class RECT(ctypes.Structure):#矩形结构
    _fields_ = (
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    )


class BITMAPINFOHEADER(ctypes.Structure):#位图信息头结构
    _fields_ = (
        ("biSize", wintypes.DWORD),
        ("biWidth", ctypes.c_long),
        ("biHeight", ctypes.c_long),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", ctypes.c_long),
        ("biYPelsPerMeter", ctypes.c_long),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    )


class BITMAPINFO(ctypes.Structure):#位图信息结构
    _fields_ = (
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3),
    )


class KeyboardHookData(ctypes.Structure):#低级键盘钩子数据结构
    _fields_ = (
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    )

WS_EX_TRANSPARENT = 0x00000020  # 窗口不拦截鼠标输入
WS_EX_TOOLWINDOW = 0x00000080  # 窗口作为工具窗口，不显示在任务栏和 Alt+Tab 中
WS_EX_LAYERED = 0x00080000  # 启用分层窗口以支持透明度等效果
WS_EX_NOACTIVATE = 0x08000000  # 显示窗口时不激活它
WS_POPUP = 0x80000000  # 创建无边框弹出窗口
ANTIALIASED_QUALITY = 4  # 使用抗锯齿字体质量
DEFAULT_CHARSET = 1  # 使用系统默认字符集
OUT_DEFAULT_PRECIS = 0  # 使用默认轮廓精度选取字体
CLIP_DEFAULT_PRECIS = 0  # 使用默认裁剪精度选取字体
FW_BOLD = 700  # 设置字体粗细为粗体
FONT_COVERAGE_SCALE = 108  # 将字体大小百分比缩放为 Window  s 像素单位
TRANSPARENT_BKMODE = 1  # 绘制文字时保留背景透明
DT_LEFT = 0x00000000  # 文本水平左对齐
DT_TOP = 0x00000000  # 文本垂直顶部对齐
DT_SINGLELINE = 0x00000020  # 文本仅绘制在单行中
DT_NOPREFIX = 0x00000800  # 禁止将 & 字符解释为助记符前缀
HWND_TOPMOST = ctypes.c_void_p(-1)  # 将窗口置于所有普通窗口之上
SWP_NOACTIVATE = 0x0010  # 设置窗口位置时不激活窗口
SWP_SHOWWINDOW = 0x0040  # 设置窗口位置时显示窗口
SWP_FRAMECHANGED = 0x0020  # 发送调整框架通知以刷新窗口边框
SW_HIDE = 0  # 隐藏窗口
SW_SHOWNOACTIVATE = 4  # 显示窗口但不激活它
ULW_ALPHA = 0x00000002  # 使用源混合因子和 Alpha 通道更新分层窗口
AC_SRC_OVER = 0  # 混合时将源图像覆盖在目标图像之上
AC_SRC_ALPHA = 1  # 使用源图像的 Alpha 通道作为混合权重


def format_time(value: datetime) -> str:#格式化时间为12小时制字符串
    return value.strftime("%I:%M %p")  # 按12小时制格式化当前时间


def transparency_to_alpha(transparency: int) -> int:#将透明度百分比转换为Alpha值
    if not MIN_TRANSPARENCY <= transparency <= MAX_TRANSPARENCY:  # 检查透明度是否在允许范围内
        raise ValueError(  # 当透明度无效时抛出异常
            f"Transparency must be between {MIN_TRANSPARENCY} and "  # 拼接错误范围的下限
            f"{MAX_TRANSPARENCY} percent."  # 拼接错误范围的上限
        )
    return round((PERCENT_SCALE - transparency) * 255 / PERCENT_SCALE)  # 按百分比换算Alpha值


def migrate_legacy_transparency(value: int) -> int:#将旧版本透明度值迁移到当前范围
    if not LEGACY_MIN_TRANSPARENCY <= value <= LEGACY_MAX_TRANSPARENCY:  # 检查旧透明度配置是否合法
        raise ValueError("Stored overlay transparency is invalid.")  # 报告无效的旧透明度值
    legacy_range = LEGACY_MAX_TRANSPARENCY - LEGACY_MIN_TRANSPARENCY  # 计算旧透明度范围
    current_range = MAX_TRANSPARENCY - MIN_TRANSPARENCY  # 计算当前透明度范围
    return round(  # 对线性映射结果取整
        MIN_TRANSPARENCY  # 保留当前范围的最小值
        + (value - LEGACY_MIN_TRANSPARENCY) * current_range / legacy_range  # 线性映射旧值
    )


def bolden_coverage(alpha: int) -> int:#将字体覆盖率的Alpha值加粗
    return min(255, (alpha * FONT_COVERAGE_SCALE + 50) // 100)  # 提升覆盖率并限制最大值


class BLENDFUNCTION(ctypes.Structure):#分层窗口混合函数结构
    _fields_ = (  # 声明Windows Alpha混合结构字段
        ("BlendOp", ctypes.c_ubyte),  # 指定混合操作
        ("BlendFlags", ctypes.c_ubyte),  # 保留供未来使用的混合标志
        ("SourceConstantAlpha", ctypes.c_ubyte),  # 指定源图像恒定透明度
        ("AlphaFormat", ctypes.c_ubyte),  # 指定源图像是否包含Alpha通道
    )


def render_clock_bgra(#渲染时钟为BGRA格式
    text: str,  # 接收要绘制的时钟文本
    font_size: int,  # 接收字体大小
    color: str,  # 接收文本颜色
    dpi: int,  # 接收屏幕缩放DPI
) -> tuple[int, int, bytes]:
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)  # 加载GDI图形接口
    user32 = ctypes.WinDLL("user32", use_last_error=True)  # 加载用户界面接口
    gdi32.CreateCompatibleDC.argtypes = (wintypes.HDC,)  # 声明兼容DC参数类型
    gdi32.CreateCompatibleDC.restype = wintypes.HDC  # 声明兼容DC返回类型
    gdi32.CreateDIBSection.argtypes = (  # 配置DIB位图参数类型
        wintypes.HDC,  # 使用兼容设备上下文
        ctypes.POINTER(BITMAPINFO),  # 接收位图格式信息
        wintypes.UINT,  # 指定使用的数据类型
        ctypes.POINTER(ctypes.c_void_p),  # 接收位图像素缓冲区地址
        wintypes.HANDLE,  # 指定共享文件句柄
        wintypes.DWORD,  # 指定共享偏移量
    )
    gdi32.CreateDIBSection.restype = wintypes.HBITMAP  # 声明DIB位图返回类型
    gdi32.CreateFontW.argtypes = (  # 配置Unicode字体创建参数类型
        ctypes.c_int,  # 字体高度
        ctypes.c_int,  # 字体宽度
        ctypes.c_int,  # 字体倾斜角度
        ctypes.c_int,  # 字符基线转向角度
        ctypes.c_int,  # 字体粗细
        wintypes.DWORD,  # 是否为斜体
        wintypes.DWORD,  # 是否带下划线
        wintypes.DWORD,  # 是否带删除线
        wintypes.DWORD,  # 字符集
        wintypes.DWORD,  # 输出精度
        wintypes.DWORD,  # 裁剪精度
        wintypes.DWORD,  # 字体输出质量
        wintypes.DWORD,  # 间距与字符集标志
        wintypes.LPCWSTR,  # 字体名称
    )
    gdi32.CreateFontW.restype = wintypes.HFONT  # 声明字体对象返回类型
    gdi32.SelectObject.argtypes = (wintypes.HDC, wintypes.HGDIOBJ)  # 声明对象选择参数类型
    gdi32.SelectObject.restype = wintypes.HGDIOBJ  # 声明对象选择返回类型
    gdi32.SetTextColor.argtypes = (wintypes.HDC, wintypes.COLORREF)  # 声明文本颜色参数类型
    gdi32.SetTextColor.restype = wintypes.COLORREF  # 声明文本颜色返回类型
    gdi32.SetBkMode.argtypes = (wintypes.HDC, ctypes.c_int)  # 声明背景模式参数类型
    gdi32.SetBkMode.restype = ctypes.c_int  # 声明背景模式返回类型
    gdi32.GetTextExtentPoint32W.argtypes = (  # 配置文本尺寸查询参数类型
        wintypes.HDC,  # 使用设备上下文
        wintypes.LPCWSTR,  # 指定待测量文本
        ctypes.c_int,  # 指定文本字符数
        ctypes.POINTER(wintypes.SIZE),  # 接收文本宽度和高度
    )
    gdi32.GetTextExtentPoint32W.restype = wintypes.BOOL  # 声明文本尺寸查询返回类型
    user32.DrawTextW.argtypes = (  # 配置文本绘制参数类型
        wintypes.HDC,  # 使用设备上下文
        wintypes.LPCWSTR,  # 指定待绘制文本
        ctypes.c_int,  # 指定文本字符数
        ctypes.POINTER(RECT),  # 指定绘制矩形
        wintypes.UINT,  # 指定绘制格式
    )
    user32.DrawTextW.restype = ctypes.c_int  # 声明文本绘制返回类型
    gdi32.DeleteObject.argtypes = (wintypes.HGDIOBJ,)  # 声明对象释放参数类型
    gdi32.DeleteObject.restype = wintypes.BOOL  # 声明对象释放返回类型
    gdi32.DeleteDC.argtypes = (wintypes.HDC,)  # 声明设备上下文释放参数类型
    gdi32.DeleteDC.restype = wintypes.BOOL  # 声明设备上下文释放返回类型

    dc = gdi32.CreateCompatibleDC(None)
    if not dc:
        raise ctypes.WinError(ctypes.get_last_error())

    font = None
    bitmap = None
    previous_font = None
    previous_bitmap = None
    try:
        pixel_height = -max(1, round(font_size * dpi / 72))
        font = gdi32.CreateFontW(
            pixel_height,
            0,
            0,
            0,
            FW_BOLD,
            0,
            0,
            0,
            DEFAULT_CHARSET,
            OUT_DEFAULT_PRECIS,
            CLIP_DEFAULT_PRECIS,
            ANTIALIASED_QUALITY,
            0,
            FONT_FAMILY,
        )
        if not font:
            raise ctypes.WinError(ctypes.get_last_error())
        previous_font = gdi32.SelectObject(dc, font)
        if not previous_font:
            raise ctypes.WinError(ctypes.get_last_error())
        gdi32.SetBkMode(dc, TRANSPARENT_BKMODE)
        red, green, blue = (
            int(color[index : index + 2], 16) for index in (1, 3, 5)
        )
        gdi32.SetTextColor(dc, 0xFFFFFF)

        text_size = wintypes.SIZE()
        if not gdi32.GetTextExtentPoint32W(
            dc, text, len(text), ctypes.byref(text_size)
        ):
            raise ctypes.WinError(ctypes.get_last_error())

        padding_x = max(1, round(dpi / 24))
        padding_y = max(1, round(dpi / 24))
        width = max(1, text_size.cx + padding_x * 2)
        height = max(1, text_size.cy + padding_y * 2)
        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = width
        bmi.bmiHeader.biHeight = -height
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        pixels_pointer = ctypes.c_void_p()
        bitmap = gdi32.CreateDIBSection(
            dc,
            ctypes.byref(bmi),
            0,
            ctypes.byref(pixels_pointer),
            None,
            0,
        )
        if not bitmap or not pixels_pointer:
            raise ctypes.WinError(ctypes.get_last_error())
        previous_bitmap = gdi32.SelectObject(dc, bitmap)
        if not previous_bitmap:
            raise ctypes.WinError(ctypes.get_last_error())
        fill_pixels = (ctypes.c_uint32 * (width * height)).from_address(
            pixels_pointer.value
        )
        for index in range(width * height):
            fill_pixels[index] = 0

        text_rect = RECT(
            padding_x, padding_y, width - padding_x, height - padding_y
        )
        if not user32.DrawTextW(
            dc,
            text,
            len(text),
            ctypes.byref(text_rect),
            DT_LEFT | DT_TOP | DT_SINGLELINE | DT_NOPREFIX,
        ):
            raise ctypes.WinError(ctypes.get_last_error())

        dib_bytes = ctypes.string_at(pixels_pointer, width * height * 4)
        bgra_pixels = bytearray(width * height * 4)
        for index in range(width * height):
            dib_index = index * 4
            alpha = bolden_coverage(max(dib_bytes[dib_index : dib_index + 3]))
            output_index = index * 4
            bgra_pixels[output_index] = (blue * alpha + 127) // 255
            bgra_pixels[output_index + 1] = (green * alpha + 127) // 255
            bgra_pixels[output_index + 2] = (red * alpha + 127) // 255
            bgra_pixels[output_index + 3] = alpha
        return width, height, bytes(bgra_pixels)
    finally:
        if previous_bitmap:
            gdi32.SelectObject(dc, previous_bitmap)
        if previous_font:
            gdi32.SelectObject(dc, previous_font)
        if bitmap:
            gdi32.DeleteObject(bitmap)
        if font:
            gdi32.DeleteObject(font)
        gdi32.DeleteDC(dc)


class NativeClockWindow:#原生时钟窗口类
    def __init__(
        self,
        user32: ctypes.WinDLL,
        kernel32: ctypes.WinDLL,
        width: int,
        height: int,
        x: int,
        y: int,
    ) -> None:
        self.user32 = user32
        self.gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
        self.class_name = f"WindowsTimeOverlayClock_{os.getpid()}"
        self.hinstance = kernel32.GetModuleHandleW(None)
        if not self.hinstance:
            raise ctypes.WinError(ctypes.get_last_error())
        self.window_proc = WNDPROC(self._window_proc)
        window_class = WNDCLASSW()
        window_class.lpfnWndProc = self.window_proc
        window_class.hInstance = self.hinstance
        window_class.lpszClassName = self.class_name
        if not self.user32.RegisterClassW(ctypes.byref(window_class)):
            raise ctypes.WinError(ctypes.get_last_error())
        self.hwnd = self.user32.CreateWindowExW(
            WS_EX_LAYERED
            | WS_EX_TRANSPARENT
            | WS_EX_TOOLWINDOW
            | WS_EX_NOACTIVATE,
            self.class_name,
            APP_PUBLISHER,
            WS_POPUP,
            x,
            y,
            width,
            height,
            None,
            None,
            self.hinstance,
            None,
        )
        if not self.hwnd:
            error = ctypes.get_last_error()
            self.user32.UnregisterClassW(self.class_name, self.hinstance)
            raise ctypes.WinError(error)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.transparency = DEFAULT_TRANSPARENCY
        self.pixels = b""
        self._configure_apis()

    def _window_proc(#窗口过程回调函数
        self, hwnd: int, message: int, wparam: int, lparam: int
    ) -> int:
        return self.user32.DefWindowProcW(hwnd, message, wparam, lparam)

    def _configure_apis(self) -> None:#配置Windows API函数参数类型和返回类型
        self.user32.UpdateLayeredWindow.argtypes = (
            wintypes.HWND,
            wintypes.HDC,
            ctypes.POINTER(POINT),
            ctypes.POINTER(wintypes.SIZE),
            wintypes.HDC,
            ctypes.POINTER(POINT),
            wintypes.DWORD,
            ctypes.POINTER(BLENDFUNCTION),
            wintypes.DWORD,
        )
        self.user32.UpdateLayeredWindow.restype = wintypes.BOOL
        self.user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
        self.user32.ShowWindow.restype = wintypes.BOOL
        self.gdi32.CreateCompatibleDC.argtypes = (wintypes.HDC,)
        self.gdi32.CreateCompatibleDC.restype = wintypes.HDC
        self.gdi32.CreateDIBSection.argtypes = (
            wintypes.HDC,
            ctypes.POINTER(BITMAPINFO),
            wintypes.UINT,
            ctypes.POINTER(ctypes.c_void_p),
            wintypes.HANDLE,
            wintypes.DWORD,
        )
        self.gdi32.CreateDIBSection.restype = wintypes.HBITMAP
        self.gdi32.SelectObject.argtypes = (
            wintypes.HDC,
            wintypes.HGDIOBJ,
        )
        self.gdi32.SelectObject.restype = wintypes.HGDIOBJ
        self.gdi32.DeleteObject.argtypes = (wintypes.HGDIOBJ,)
        self.gdi32.DeleteObject.restype = wintypes.BOOL
        self.gdi32.DeleteDC.argtypes = (wintypes.HDC,)
        self.gdi32.DeleteDC.restype = wintypes.BOOL

    def update(#更新窗口内容
        self,
        pixels: bytes,
        width: int,
        height: int,
        x: int,
        y: int,
        transparency: int,
    ) -> None:
        alpha = transparency_to_alpha(transparency)
        dc = self.gdi32.CreateCompatibleDC(None)
        if not dc:
            raise ctypes.WinError(ctypes.get_last_error())
        bitmap = None
        previous_bitmap = None
        try:
            bmi = BITMAPINFO()
            bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bmi.bmiHeader.biWidth = width
            bmi.bmiHeader.biHeight = -height
            bmi.bmiHeader.biPlanes = 1
            bmi.bmiHeader.biBitCount = 32
            bmi.bmiHeader.biCompression = 0
            pixels_pointer = ctypes.c_void_p()
            bitmap = self.gdi32.CreateDIBSection(
                dc,
                ctypes.byref(bmi),
                0,
                ctypes.byref(pixels_pointer),
                None,
                0,
            )
            if not bitmap or not pixels_pointer:
                raise ctypes.WinError(ctypes.get_last_error())
            previous_bitmap = self.gdi32.SelectObject(dc, bitmap)
            if not previous_bitmap:
                raise ctypes.WinError(ctypes.get_last_error())
            ctypes.memmove(pixels_pointer, pixels, len(pixels))
            destination = POINT(x, y)
            size = wintypes.SIZE(width, height)
            source = POINT(0, 0)
            blend = BLENDFUNCTION(AC_SRC_OVER, 0, alpha, AC_SRC_ALPHA)
            if not self.user32.UpdateLayeredWindow(
                self.hwnd,
                None,
                ctypes.byref(destination),
                ctypes.byref(size),
                dc,
                ctypes.byref(source),
                0,
                ctypes.byref(blend),
                ULW_ALPHA,
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            self.pixels = pixels
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.transparency = transparency
        finally:
            if previous_bitmap:
                self.gdi32.SelectObject(dc, previous_bitmap)
            if bitmap:
                self.gdi32.DeleteObject(bitmap)
            self.gdi32.DeleteDC(dc)

    def set_transparency(self, transparency: int) -> None:#设置窗口透明度
        if self.pixels:
            self.update(
                self.pixels,
                self.width,
                self.height,
                self.x,
                self.y,
                transparency,
            )
        else:
            self.transparency = transparency

    def show(self) -> None:#显示窗口
        self.user32.ShowWindow(self.hwnd, SW_SHOWNOACTIVATE)

    def hide(self) -> None:#隐藏窗口
        self.user32.ShowWindow(self.hwnd, SW_HIDE)

    def close(self) -> None:#关闭窗口并注销窗口类
        if self.hwnd:#
            self.user32.DestroyWindow(self.hwnd)
            self.hwnd = None
        if self.hinstance:#
            self.user32.UnregisterClassW(self.class_name, self.hinstance)
            self.hinstance = None


def enable_high_dpi_awareness() -> None:#启用高DPI感知
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    try:
        set_awareness = user32.SetProcessDpiAwarenessContext
    except AttributeError:
        set_awareness = None
    if set_awareness is not None:
        set_awareness.argtypes = (ctypes.c_void_p,)
        set_awareness.restype = wintypes.BOOL
        if set_awareness(ctypes.c_void_p(-4)):
            return
        if ctypes.get_last_error() == 5:
            return

    try:
        shcore = ctypes.WinDLL("shcore", use_last_error=True)
        set_awareness = shcore.SetProcessDpiAwareness
    except (AttributeError, OSError):
        set_awareness = None
    if set_awareness is not None:
        set_awareness.argtypes = (ctypes.c_int,)
        set_awareness.restype = ctypes.c_long
        result = set_awareness(2)
        if result in (0, -2147024891):
            return

    try:
        set_awareness = user32.SetProcessDPIAware
    except AttributeError:
        return
    set_awareness.argtypes = ()
    set_awareness.restype = wintypes.BOOL
    if not set_awareness() and ctypes.get_last_error() not in (0, 5):
        raise ctypes.WinError(ctypes.get_last_error())


def acquire_single_instance_mutex() -> wintypes.HANDLE | None:#获取单实例互斥体
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.argtypes = (
        wintypes.LPVOID,
        wintypes.BOOL,
        wintypes.LPCWSTR,
    )
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL

    ctypes.set_last_error(0)
    mutex = kernel32.CreateMutexW(
        None, False, SINGLE_INSTANCE_MUTEX_NAME
    )
    if not mutex:
        raise ctypes.WinError(ctypes.get_last_error())
    if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
        if not kernel32.CloseHandle(mutex):
            raise ctypes.WinError(ctypes.get_last_error())
        return None
    return mutex


def supports_dwm_rounded_corners(build: int) -> bool:
    return build >= 22000


def apply_rounded_corners(window: tk.Misc) -> bool:
    window.update_idletasks()
    if not window.winfo_ismapped():
        return False

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.GetAncestor.argtypes = (wintypes.HWND, wintypes.UINT)
    user32.GetAncestor.restype = wintypes.HWND
    hwnd = user32.GetAncestor(wintypes.HWND(window.winfo_id()), 2)
    if not hwnd:
        return False

    if supports_dwm_rounded_corners(sys.getwindowsversion().build):
        dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)
        dwmapi.DwmSetWindowAttribute.argtypes = (
            wintypes.HWND,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.DWORD,
        )
        dwmapi.DwmSetWindowAttribute.restype = ctypes.c_long
        corner_preference = ctypes.c_int(2)
        result = dwmapi.DwmSetWindowAttribute(
            hwnd,
            33,
            ctypes.byref(corner_preference),
            ctypes.sizeof(corner_preference),
        )
        if result == 0:
            return True

    rect = RECT()
    user32.GetWindowRect.argtypes = (
        wintypes.HWND,
        ctypes.POINTER(RECT),
    )
    user32.GetWindowRect.restype = wintypes.BOOL
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        raise ctypes.WinError(ctypes.get_last_error())
    width = rect.right - rect.left
    height = rect.bottom - rect.top

    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
    gdi32.CreateRoundRectRgn.argtypes = (
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    )
    gdi32.CreateRoundRectRgn.restype = wintypes.HANDLE
    region = gdi32.CreateRoundRectRgn(0, 0, width + 1, height + 1, 18, 18)
    if not region:
        raise ctypes.WinError(ctypes.get_last_error())

    user32.SetWindowRgn.argtypes = (
        wintypes.HWND,
        wintypes.HANDLE,
        wintypes.BOOL,
    )
    user32.SetWindowRgn.restype = ctypes.c_int
    if not user32.SetWindowRgn(hwnd, region, True):
        error = ctypes.get_last_error()
        gdi32.DeleteObject.argtypes = (wintypes.HANDLE,)
        gdi32.DeleteObject.restype = wintypes.BOOL
        gdi32.DeleteObject(region)
        raise ctypes.WinError(error)
    return True


def schedule_rounded_corners(window: tk.Toplevel) -> None:
    scheduled_id: str | None = None
    applied_size: tuple[int, int] | None = None

    def apply_when_ready(event: tk.Event | None = None) -> None:
        nonlocal scheduled_id, applied_size
        if event is not None and event.widget is not window:
            return
        if scheduled_id is not None:
            try:
                window.after_cancel(scheduled_id)
            except tk.TclError:
                return
            scheduled_id = None

        try:
            if not window.winfo_exists():
                return
            if not window.winfo_ismapped():
                scheduled_id = window.after(50, apply_when_ready)
                return
            size = (window.winfo_width(), window.winfo_height())
            if size[0] <= 1 or size[1] <= 1:
                scheduled_id = window.after(50, apply_when_ready)
                return
            if size == applied_size:
                return
            if apply_rounded_corners(window):
                applied_size = size
        except tk.TclError:
            return

    def schedule(event: tk.Event) -> None:
        nonlocal scheduled_id
        if event.widget is not window:
            return
        if scheduled_id is not None:
            try:
                window.after_cancel(scheduled_id)
            except tk.TclError:
                return
        scheduled_id = window.after(50, apply_when_ready)

    window.bind("<Map>", schedule, add="+")
    window.bind("<Configure>", schedule, add="+")
    window.after(100, apply_when_ready)


def load_time_icon(user32) -> int:
    icon_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tray_icon.ico"
    )
    if not os.path.isfile(icon_path):
        raise FileNotFoundError(f"Tray icon file not found: {icon_path}")

    user32.LoadImageW.argtypes = (
        wintypes.HINSTANCE,
        wintypes.LPCWSTR,
        wintypes.UINT,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.UINT,
    )
    user32.LoadImageW.restype = wintypes.HANDLE
    image_icon = 1
    load_from_file = 0x0010
    default_size = 0x0040
    icon = user32.LoadImageW(
        None, icon_path, image_icon, 0, 0, load_from_file | default_size
    )
    if not icon:
        raise ctypes.WinError(ctypes.get_last_error())
    return icon


def shortcut_for_key(
    key: int, ctrl_down: bool, shift_down: bool
) -> str | None:
    if not ctrl_down:
        return None
    if key in ARROW_KEYS:
        return ARROW_KEYS[key]
    if key == VK_QUIT and shift_down:
        return "quit"
    return None


class MovementController:
    def __init__(
        self,
        minimum_speed: float = 30.0,
        maximum_speed: float = 420.0,
        acceleration_duration: float = 1.0,
        acceleration: float = 1400.0,
        deceleration: float = 560.0,
    ) -> None:
        self.minimum_speed = minimum_speed
        self.maximum_speed = maximum_speed
        self.acceleration_duration = acceleration_duration
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.pressed_keys: set[str] = set()
        self.held_duration = 0.0
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def set_key(self, direction: str, pressed: bool) -> None:
        if pressed:
            if direction not in self.pressed_keys:
                if not self.pressed_keys:
                    self.held_duration = 0.0
                self.pressed_keys.add(direction)
        else:
            self.pressed_keys.discard(direction)
            if not self.pressed_keys:
                self.held_duration = 0.0

    def clear_keys(self) -> None:
        self.pressed_keys.clear()
        self.held_duration = 0.0

    def update(self, elapsed: float) -> tuple[float, float]:
        elapsed = min(max(elapsed, 0.0), 0.05)
        if elapsed == 0.0:
            return 0.0, 0.0

        direction_x = float(
            ("right" in self.pressed_keys) - ("left" in self.pressed_keys)
        )
        direction_y = float(
            ("down" in self.pressed_keys) - ("up" in self.pressed_keys)
        )
        if direction_x or direction_y:
            if direction_x and direction_y:
                diagonal_scale = 1 / math.sqrt(2)
                direction_x *= diagonal_scale
                direction_y *= diagonal_scale
            self.held_duration += elapsed
            progress = min(self.held_duration / self.acceleration_duration, 1.0)
            eased_progress = progress * (2 - progress)
            speed = self.minimum_speed + (
                self.maximum_speed - self.minimum_speed
            ) * eased_progress
            target_x = direction_x * speed
            target_y = direction_y * speed
            velocity_change_x = target_x - self.velocity_x
            velocity_change_y = target_y - self.velocity_y
            velocity_change = math.hypot(velocity_change_x, velocity_change_y)
            max_change = self.acceleration * elapsed
            if velocity_change > max_change:
                scale = max_change / velocity_change
                velocity_change_x *= scale
                velocity_change_y *= scale
            self.velocity_x += velocity_change_x
            self.velocity_y += velocity_change_y
        else:
            speed = math.hypot(self.velocity_x, self.velocity_y)
            if speed:
                new_speed = max(0.0, speed - self.deceleration * elapsed)
                scale = new_speed / speed
                self.velocity_x *= scale
                self.velocity_y *= scale

        return self.velocity_x * elapsed, self.velocity_y * elapsed


def make_startup_command(python_executable: str, script_path: str) -> str:
    executable_name = os.path.basename(python_executable).lower()
    if executable_name == "python.exe":
        python_executable = os.path.join(
            os.path.dirname(python_executable), "pythonw.exe"
        )
    return subprocess.list2cmdline(
        [python_executable, os.path.abspath(script_path)]
    )


def is_autostart_enabled() -> bool:
    import winreg

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
        ) as key:
            value, _ = winreg.QueryValueEx(key, AUTOSTART_VALUE_NAME)
    except FileNotFoundError:
        return False
    return value == make_startup_command(sys.executable, __file__)


def set_autostart_enabled(enabled: bool) -> None:
    import winreg

    with winreg.CreateKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
    ) as key:
        if enabled:
            winreg.SetValueEx(
                key,
                AUTOSTART_VALUE_NAME,
                0,
                winreg.REG_SZ,
                make_startup_command(sys.executable, __file__),
            )
        else:
            try:
                winreg.DeleteValue(key, AUTOSTART_VALUE_NAME)
            except FileNotFoundError:
                pass


def load_display_settings() -> tuple[int, str, int]:
    import winreg

    font_size = 32
    clock_color = COLOR_PRESETS[0][1]
    transparency = DEFAULT_TRANSPARENCY
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SETTINGS_KEY_PATH)
    except FileNotFoundError:
        return font_size, clock_color, transparency

    with key:
        try:
            font_size, value_type = winreg.QueryValueEx(key, "FontSize")
            if (
                value_type != winreg.REG_DWORD
                or not isinstance(font_size, int)
                or not 12 <= font_size <= 96
            ):
                raise ValueError("Stored clock font size is invalid.")
        except FileNotFoundError:
            font_size = 32
        try:
            clock_color, value_type = winreg.QueryValueEx(key, "ClockColor")
            if (
                value_type != winreg.REG_SZ
                or not isinstance(clock_color, str)
                or not is_hex_color(clock_color)
            ):
                raise ValueError("Stored clock color is invalid.")
        except FileNotFoundError:
            clock_color = COLOR_PRESETS[0][1]
        try:
            transparency, value_type = winreg.QueryValueEx(
                key, "Transparency"
            )
        except FileNotFoundError:
            try:
                legacy_value, value_type = winreg.QueryValueEx(key, "Opacity")
            except FileNotFoundError:
                transparency = DEFAULT_TRANSPARENCY
            else:
                if (
                    value_type != winreg.REG_DWORD
                    or not isinstance(legacy_value, int)
                ):
                    raise ValueError("Stored overlay transparency is invalid.")
                transparency = migrate_legacy_transparency(legacy_value)
                save_display_setting("Transparency", transparency)
        else:
            if (
                value_type != winreg.REG_DWORD
                or not isinstance(transparency, int)
                or not MIN_TRANSPARENCY
                <= transparency
                <= MAX_TRANSPARENCY
            ):
                raise ValueError("Stored overlay transparency is invalid.")
    return font_size, clock_color, transparency


def save_display_setting(name: str, value: int | str) -> None:
    import winreg

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, SETTINGS_KEY_PATH) as key:
        if isinstance(value, int):
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
        else:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)


def is_hex_color(value: str) -> bool:
    return (
        len(value) == 7
        and value.startswith("#")
        and all(character in "0123456789abcdefABCDEF" for character in value[1:])
    )


def clamp_position(
    x: int,
    y: int,
    window_width: int,
    window_height: int,
    bounds: tuple[int, int, int, int],
) -> tuple[int, int]:
    left, top, width, height = bounds
    max_x = left + max(0, width - window_width)
    max_y = top + max(0, height - window_height)
    return min(max(x, left), max_x), min(max(y, top), max_y)


def point_inside_bounds(
    x: int, y: int, bounds: tuple[int, int, int, int]
) -> bool:
    left, top, right, bottom = bounds
    return left <= x < right and top <= y < bottom


def tray_menu_position(
    cursor_x: int,
    cursor_y: int,
    menu_width: int,
    menu_height: int,
    bounds: tuple[int, int, int, int],
) -> tuple[int, int]:
    x, y = clamp_position(
        cursor_x + 4,
        cursor_y - 23,
        menu_width,
        menu_height,
        bounds,
    )
    return clamp_position(
        x,
        y - TRAY_MENU_EXTRA_UPWARD_OFFSET,
        menu_width,
        menu_height,
        bounds,
    )


class TimeOverlay:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.user32 = ctypes.WinDLL("user32", use_last_error=True)
        self.shell32 = ctypes.WinDLL("shell32", use_last_error=True)
        self._configure_win32()
        self.shortcut_queue: queue.SimpleQueue[str] = queue.SimpleQueue()
        self.tray_queue: queue.SimpleQueue[str] = queue.SimpleQueue()
        self.keyboard_hook_handle = None
        self.tray_icon: TrayIcon | None = None
        self.movement = MovementController()
        self.x = 10
        self.y = 10
        self.precise_x = float(self.x)
        self.precise_y = float(self.y)
        self.last_movement_update = time.perf_counter()
        self.clock_visible = True
        self.autostart_enabled = is_autostart_enabled()
        (
            self.font_size,
            self.clock_color,
            self.transparency,
        ) = load_display_settings()
        self.root.title(APP_PUBLISHER)
        self.root.overrideredirect(True)
        self.root.geometry("1x1-32000-32000")
        self.root.attributes("-alpha", 0.0)
        self.root.deiconify()
        self.tray_menu: tk.Toplevel | None = None
        self.tray_menu_bounds: tuple[int, int, int, int] | None = None
        self.tray_menu_dismiss_queued = False
        self.mouse_hook_handle = None
        self.root.bind_all(
            "<Button-1>", self._close_tray_menu_on_outside_click, add="+"
        )
        self.clock_text = ""
        self.width = 1
        self.height = 1
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel32.GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)
        self.kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE
        self.clock_window = NativeClockWindow(
            self.user32,
            self.kernel32,
            self.width,
            self.height,
            self.x,
            self.y,
        )
        self.hwnd = self.clock_window.hwnd
        try:
            self._install_keyboard_hook()
            self.tray_icon = TrayIcon(self, self.tray_queue)
        except OSError:
            if self.tray_icon is not None:
                self.tray_icon.close()
            self._uninstall_keyboard_hook()
            self.clock_window.close()
            raise
        self._refresh_clock()
        self.root.after(25, self._process_actions)
        self.root.after(16, self._update_movement)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _configure_win32(self) -> None:
        self.user32.SetWindowsHookExW.argtypes = (
            ctypes.c_int,
            HOOKPROC,
            wintypes.HINSTANCE,
            wintypes.DWORD,
        )
        self.user32.SetWindowsHookExW.restype = wintypes.HANDLE
        self.user32.UnhookWindowsHookEx.argtypes = (wintypes.HANDLE,)
        self.user32.UnhookWindowsHookEx.restype = wintypes.BOOL
        self.user32.CallNextHookEx.argtypes = (
            wintypes.HANDLE,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        )
        self.user32.CallNextHookEx.restype = ctypes.c_ssize_t
        self.user32.GetAsyncKeyState.argtypes = (ctypes.c_int,)
        self.user32.GetAsyncKeyState.restype = ctypes.c_short
        self.user32.SetWindowPos.argtypes = (
            wintypes.HWND,
            wintypes.HWND,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.UINT,
        )
        self.user32.SetWindowPos.restype = wintypes.BOOL
        self.user32.GetSystemMetrics.argtypes = (ctypes.c_int,)
        self.user32.GetSystemMetrics.restype = ctypes.c_int
        self.user32.RegisterClassW.argtypes = (ctypes.POINTER(WNDCLASSW),)
        self.user32.RegisterClassW.restype = wintypes.ATOM
        self.user32.CreateWindowExW.argtypes = (
            wintypes.DWORD,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.DWORD,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.HWND,
            wintypes.HMENU,
            wintypes.HINSTANCE,
            wintypes.LPVOID,
        )
        self.user32.CreateWindowExW.restype = wintypes.HWND
        self.user32.DestroyWindow.argtypes = (wintypes.HWND,)
        self.user32.DestroyWindow.restype = wintypes.BOOL
        self.user32.UnregisterClassW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.HINSTANCE,
        )
        self.user32.UnregisterClassW.restype = wintypes.BOOL
        self.user32.DefWindowProcW.argtypes = (
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        )
        self.user32.DefWindowProcW.restype = wintypes.LPARAM
        self.user32.LoadIconW.argtypes = (wintypes.HINSTANCE, wintypes.LPCWSTR)
        self.user32.LoadIconW.restype = wintypes.HICON
        self.user32.DestroyIcon.argtypes = (wintypes.HICON,)
        self.user32.DestroyIcon.restype = wintypes.BOOL
        self.user32.GetCursorPos.argtypes = (ctypes.POINTER(POINT),)
        self.user32.GetCursorPos.restype = wintypes.BOOL
        self.shell32.Shell_NotifyIconW.argtypes = (
            wintypes.DWORD,
            ctypes.POINTER(NOTIFYICONDATAW),
        )
        self.shell32.Shell_NotifyIconW.restype = wintypes.BOOL

    def _install_keyboard_hook(self) -> None:
        self.keyboard_hook_proc = HOOKPROC(self._on_keyboard_event)
        self.keyboard_hook_handle = self.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL, self.keyboard_hook_proc, None, 0
        )
        if not self.keyboard_hook_handle:
            raise ctypes.WinError(ctypes.get_last_error())

    def _uninstall_keyboard_hook(self) -> None:
        if self.keyboard_hook_handle:
            self.user32.UnhookWindowsHookEx(self.keyboard_hook_handle)
            self.keyboard_hook_handle = None

    def _on_keyboard_event(
        self, code: int, message: int, data_pointer: int
    ) -> int:
        if code >= 0 and message in (
            WM_KEYDOWN,
            WM_KEYUP,
            WM_SYSKEYDOWN,
            WM_SYSKEYUP,
        ):
            key = ctypes.cast(
                data_pointer, ctypes.POINTER(KeyboardHookData)
            ).contents.vkCode
            key_down = message in (WM_KEYDOWN, WM_SYSKEYDOWN)
            if key in (VK_CONTROL,):
                if not key_down:
                    self.movement.clear_keys()
            elif key in (0xA2, 0xA3):
                if not key_down and not (
                    self.user32.GetAsyncKeyState(VK_CONTROL) & CTRL_DOWN_MASK
                ):
                    self.movement.clear_keys()
            elif key in ARROW_KEYS:
                if key_down:
                    ctrl_down = bool(
                        self.user32.GetAsyncKeyState(VK_CONTROL)
                        & CTRL_DOWN_MASK
                    )
                    self.movement.set_key(ARROW_KEYS[key], ctrl_down)
                else:
                    self.movement.set_key(ARROW_KEYS[key], False)
            elif key_down and key == VK_QUIT:
                ctrl_down = bool(
                    self.user32.GetAsyncKeyState(VK_CONTROL) & CTRL_DOWN_MASK
                )
                shift_down = bool(
                    self.user32.GetAsyncKeyState(VK_SHIFT) & CTRL_DOWN_MASK
                )
                if shortcut_for_key(key, ctrl_down, shift_down) == "quit":
                    self.shortcut_queue.put("quit")
        return self.user32.CallNextHookEx(
            self.keyboard_hook_handle, code, message, data_pointer
        )

    def _set_window_position(self, x: int, y: int, show: bool = False) -> None:
        flags = SWP_NOACTIVATE | SWP_FRAMECHANGED
        if show:
            flags |= SWP_SHOWWINDOW
        if not self.user32.SetWindowPos(
            self.hwnd, HWND_TOPMOST, x, y, self.width, self.height, flags
        ):
            raise ctypes.WinError(ctypes.get_last_error())

    def _virtual_screen_bounds(self) -> tuple[int, int, int, int]:
        return (
            self.user32.GetSystemMetrics(76),
            self.user32.GetSystemMetrics(77),
            self.user32.GetSystemMetrics(78),
            self.user32.GetSystemMetrics(79),
        )

    def _show_tray_menu(self) -> None:
        if self.tray_icon is None:
            return
        try:
            self.tray_icon._show_context_menu()
        except (OSError, tk.TclError) as error:
            messagebox.showerror(APP_PUBLISHER, str(error), parent=self.root)

    def _close_tray_menu_on_outside_click(self, event: tk.Event) -> None:
        menu = self.tray_menu
        if menu is None:
            return
        try:
            if event.widget.winfo_toplevel() is menu:
                return
        except tk.TclError:
            pass
        self._dismiss_tray_menu()

    def _install_mouse_hook(self) -> None:
        self.mouse_hook_proc = HOOKPROC(self._on_mouse_event)
        self.mouse_hook_handle = self.user32.SetWindowsHookExW(
            WH_MOUSE_LL, self.mouse_hook_proc, None, 0
        )
        if not self.mouse_hook_handle:
            raise ctypes.WinError(ctypes.get_last_error())

    def _uninstall_mouse_hook(self) -> None:
        if self.mouse_hook_handle:
            self.user32.UnhookWindowsHookEx(self.mouse_hook_handle)
            self.mouse_hook_handle = None

    def _on_mouse_event(
        self, code: int, message: int, data_pointer: int
    ) -> int:
        if (
            code >= 0
            and message
            in (
                WM_LBUTTONDOWN,
                WM_RBUTTONDOWN,
                WM_MBUTTONDOWN,
                WM_XBUTTONDOWN,
            )
            and self.tray_menu_bounds is not None
            and not self.tray_menu_dismiss_queued
        ):
            mouse = ctypes.cast(
                data_pointer, ctypes.POINTER(MSLLHOOKSTRUCT)
            ).contents
            if not point_inside_bounds(
                mouse.pt.x, mouse.pt.y, self.tray_menu_bounds
            ):
                self.tray_menu_dismiss_queued = True
                self.tray_queue.put("dismiss_menu")
        return self.user32.CallNextHookEx(
            self.mouse_hook_handle, code, message, data_pointer
        )

    def _dismiss_tray_menu(self) -> None:
        menu = self.tray_menu
        self.tray_menu = None
        self.tray_menu_bounds = None
        self.tray_menu_dismiss_queued = False
        self._uninstall_mouse_hook()
        if menu is not None:
            try:
                if menu.winfo_exists():
                    menu.destroy()
            except tk.TclError:
                pass

    def _process_actions(self) -> None:
        while not self.shortcut_queue.empty():
            shortcut = self.shortcut_queue.get()
            if shortcut == "quit":
                self.close()
                return
        while not self.tray_queue.empty():
            action = self.tray_queue.get()
            if action == "show_menu":
                self._show_tray_menu()
            elif action == "dismiss_menu":
                self._dismiss_tray_menu()
            elif action == "toggle_clock":
                self._toggle_clock_visibility()
            elif action == "toggle_autostart":
                self._toggle_autostart()
            elif action == "quit":
                self.close()
                return
            elif action == "custom_size":
                self._ask_custom_size()
            elif action == "custom_color":
                self._ask_custom_color()
            elif action == "transparency":
                self._show_transparency_dialog()
            elif action.startswith("size:"):
                self._set_font_size(int(action.removeprefix("size:")))
            elif action.startswith("color:"):
                self._set_clock_color(action.removeprefix("color:"))
            elif action.startswith("error:"):
                messagebox.showerror(
                    APP_PUBLISHER,
                    action.removeprefix("error:"),
                    parent=self.root,
                )
        self.root.after(25, self._process_actions)

    def _show_transparency_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("悬浮窗透明度")
        dialog.transient(self.root)
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        original_transparency = self.transparency
        transparency_value = tk.IntVar(value=self.transparency)
        value_label = tk.Label(dialog, text=f"{self.transparency}%")
        value_label.pack(padx=16, pady=(14, 0))

        def preview(value: str) -> None:
            transparency = int(float(value))
            value_label.configure(text=f"{transparency}%")
            self.clock_window.set_transparency(transparency)

        slider = tk.Scale(
            dialog,
            from_=MIN_TRANSPARENCY,
            to=MAX_TRANSPARENCY,
            orient=tk.HORIZONTAL,
            variable=transparency_value,
            showvalue=False,
            length=280,
            command=preview,
        )
        slider.pack(padx=16, pady=8)

        buttons = tk.Frame(dialog)
        buttons.pack(padx=16, pady=(0, 14), fill=tk.X)

        def cancel() -> None:
            self.clock_window.set_transparency(original_transparency)
            dialog.destroy()

        def save() -> None:
            transparency = transparency_value.get()
            try:
                save_display_setting("Transparency", transparency)
            except OSError as error:
                messagebox.showerror(
                    APP_PUBLISHER, str(error), parent=dialog
                )
                return
            self.transparency = transparency
            self.clock_window.set_transparency(transparency)
            dialog.destroy()

        tk.Button(buttons, text="取消", command=cancel).pack(side=tk.RIGHT)
        tk.Button(buttons, text="应用", command=save).pack(
            side=tk.RIGHT, padx=(0, 8)
        )
        dialog.protocol("WM_DELETE_WINDOW", cancel)
        dialog.grab_set()
        schedule_rounded_corners(dialog)

    def _update_movement(self) -> None:
        if not self.root.winfo_exists():
            return
        ctrl_down = bool(
            self.user32.GetAsyncKeyState(VK_CONTROL) & CTRL_DOWN_MASK
        )
        if not ctrl_down:
            self.movement.clear_keys()
        now = time.perf_counter()
        elapsed = now - self.last_movement_update
        self.last_movement_update = now
        dx, dy = self.movement.update(elapsed)
        if dx or dy:
            self._move_overlay(dx, dy)
        self.root.after(16, self._update_movement)

    def _set_font_size(self, size: int) -> None:
        try:
            save_display_setting("FontSize", size)
        except OSError as error:
            messagebox.showerror(APP_PUBLISHER, str(error), parent=self.root)
            return
        self.font_size = size
        self.clock_text = ""
        self._refresh_clock()
        self._resize_to_content()

    def _ask_custom_size(self) -> None:
        size = simpledialog.askinteger(
            "时间字号",
            "输入字号（12–96）：",
            parent=self.root,
            initialvalue=self.font_size,
            minvalue=12,
            maxvalue=96,
        )
        if size is not None:
            self._set_font_size(size)

    def _set_clock_color(self, color: str) -> None:
        if not is_hex_color(color):
            messagebox.showerror("时间颜色", "颜色格式无效。", parent=self.root)
            return
        try:
            save_display_setting("ClockColor", color)
        except OSError as error:
            messagebox.showerror(APP_PUBLISHER, str(error), parent=self.root)
            return
        self.clock_color = color
        self.clock_text = ""
        self._refresh_clock()

    def _ask_custom_color(self) -> None:
        color = colorchooser.askcolor(
            color=self.clock_color, title="选择时间颜色", parent=self.root
        )[1]
        if color:
            self._set_clock_color(color)

    def _resize_to_content(self) -> None:
        self.x, self.y = clamp_position(
            self.x,
            self.y,
            self.width,
            self.height,
            self._virtual_screen_bounds(),
        )
        self.precise_x = float(self.x)
        self.precise_y = float(self.y)
        self._set_window_position(self.x, self.y, show=self.clock_visible)

    def _toggle_clock_visibility(self) -> None:
        if self.clock_visible:
            self.clock_window.hide()
            self.clock_visible = False
        else:
            self.clock_window.show()
            self.clock_visible = True

    def _toggle_autostart(self) -> None:
        enabled = not self.autostart_enabled
        try:
            set_autostart_enabled(enabled)
        except (OSError, ValueError) as error:
            messagebox.showerror(APP_PUBLISHER, str(error), parent=self.root)
            return
        self.autostart_enabled = enabled

    def _move_overlay(self, dx: float, dy: float) -> None:
        self.precise_x += dx
        self.precise_y += dy
        target_x = round(self.precise_x)
        target_y = round(self.precise_y)
        clamped_x, clamped_y = clamp_position(
            target_x,
            target_y,
            self.width,
            self.height,
            self._virtual_screen_bounds(),
        )
        if (clamped_x, clamped_y) != (target_x, target_y):
            self.precise_x = float(clamped_x)
            self.precise_y = float(clamped_y)
        if (clamped_x, clamped_y) == (self.x, self.y):
            return
        self.x, self.y = clamped_x, clamped_y
        self._set_window_position(self.x, self.y)

    def _refresh_clock(self) -> None:
        text = format_time(datetime.now())
        if text != self.clock_text:
            dpi = max(1, round(self.root.winfo_fpixels("1i")))
            width, height, pixels = render_clock_bgra(
                text, self.font_size, self.clock_color, dpi
            )
            self.width = width
            self.height = height
            self.clock_text = text
            self._resize_to_content()
            self.clock_window.update(
                pixels,
                width,
                height,
                self.x,
                self.y,
                self.transparency,
            )
            if self.clock_visible:
                self.clock_window.show()
        self.root.after(1000, self._refresh_clock)

    def close(self) -> None:
        if self.tray_icon is not None:
            self.tray_icon.close()
        self._dismiss_tray_menu()
        self._uninstall_keyboard_hook()
        self.clock_window.close()
        self.root.destroy()


class TrayIcon:  # 定义系统托盘图标及其菜单控制器
    def __init__(  # 初始化托盘图标控制器
        self,  # 接收当前托盘对象
        overlay: TimeOverlay,  # 接收悬浮窗实例
        action_queue: queue.SimpleQueue[str],  # 接收托盘操作队列
    ) -> None:
        self.overlay = overlay  # 保存悬浮窗实例
        self.user32 = overlay.user32  # 保存 Win32 用户接口模块
        self.shell32 = overlay.shell32  # 保存 Win32 Shell 接口模块
        self.action_queue = action_queue  # 保存动作队列引用
        self.class_name = f"WindowsTimeOverlayTray_{os.getpid()}"  # 为托盘窗口生成唯一类名
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # 加载内核接口库
        self.kernel32.GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)  # 设置模块句柄函数参数类型
        self.kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE  # 设置模块句柄函数返回类型
        self.instance = self.kernel32.GetModuleHandleW(None)  # 获取当前应用实例句柄
        self.window_proc = WNDPROC(self._window_proc)  # 创建托盘窗口回调函数
        self.hwnd = None  # 初始化托盘窗口句柄
        self.icon_data = NOTIFYICONDATAW()  # 创建托盘图标数据结构

        window_class = WNDCLASSW()  # 创建托盘窗口类结构
        window_class.lpfnWndProc = self.window_proc  # 指定窗口消息处理函数
        window_class.hInstance = self.instance  # 指定窗口所属实例
        window_class.lpszClassName = self.class_name  # 指定窗口类名称
        if not self.user32.RegisterClassW(ctypes.byref(window_class)):  # 注册托盘窗口类
            raise ctypes.WinError(ctypes.get_last_error())  # 注册失败时抛出 Windows 错误

        self.hwnd = self.user32.CreateWindowExW(  # 创建不可见托盘消息窗口
            0,  # 不应用扩展窗口样式
            self.class_name,  # 使用已注册的窗口类名
            APP_PUBLISHER,  # 设置窗口标题
            0,  # 不应用普通窗口样式
            0,  # 设置初始横坐标
            0,  # 设置初始纵坐标
            0,  # 设置初始窗口宽度
            0,  # 设置初始窗口高度
            None,  # 不指定父窗口
            None,  # 不指定菜单
            self.instance,  # 指定应用实例句柄
            None,  # 不传递附加创建参数
        )
        if not self.hwnd:  # 棱查托盘窗口是否创建成功
            self.user32.UnregisterClassW(self.class_name, self.instance)  # 创建失败时注销窗口类
            raise ctypes.WinError(ctypes.get_last_error())  # 抛出窗口创建失败错误

        self.icon_data.cbSize = ctypes.sizeof(self.icon_data)  # 设置托盘数据结构大小
        self.icon_data.hWnd = self.hwnd  # 将托盘图标绑定到消息窗口
        self.icon_data.uID = 1  # 设置托盘图标唯一标识
        self.icon_data.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP  # 设置图标、消息和提示标志
        self.icon_data.uCallbackMessage = TRAY_CALLBACK_MESSAGE  # 设置托盘回调消息编号
        self.icon_data.hIcon = load_time_icon(self.user32)  # 加载托盘图标句柄
        self.icon_data.szTip = APP_PUBLISHER  # 设置托盘悬停提示文本
        if not self.shell32.Shell_NotifyIconW(  # 尝试添加托盘图标
            NIM_ADD, ctypes.byref(self.icon_data)  # 指定添加操作及图标数据
        ):
            self.user32.DestroyIcon(self.icon_data.hIcon)  # 添加失败时销毁图标
            self.user32.DestroyWindow(self.hwnd)  # 销毁托盘消息窗口
            self.user32.UnregisterClassW(self.class_name, self.instance)  # 注销托盘窗口类
            raise ctypes.WinError(ctypes.get_last_error())  # 抛出托盘图标添加失败错误

    def _window_proc(  # 定义托盘窗口消息处理函数
        self,  # 接收托盘对象
        hwnd: int,  # 接收窗口句柄
        message: int,  # 接收窗口消息类型
        wparam: int,  # 接收消息附加参数
        lparam: int,  # 接收消息附加参数
    ) -> int:
        if message == TRAY_CALLBACK_MESSAGE:  # 判断是否收到托盘回调消息
            if lparam == WM_LBUTTONUP:  # 判断是否点击托盘左键
                self.action_queue.put("show_menu")  # 将打开菜单动作加入队列
            return 0  # 已处理托盘回调消息
        if message == WM_CLOSE:  # 判断是否收到窗口关闭消息
            return 0  # 阻止托盘窗口被直接关闭
        return self.user32.DefWindowProcW(hwnd, message, wparam, lparam)  # 将其他消息交给系统默认处理

    def _show_context_menu(self) -> None:  # 创建并显示托盘右键菜单
        existing_menu = self.overlay.tray_menu  # 获取当前托盘菜单对象
        if existing_menu is not None:  # 判断已有菜单是否存在
            try:
                if existing_menu.winfo_exists():  # 棱查已有菜单是否仍有效
                    existing_menu.lift()  # 将已有菜单置于前台
                    existing_menu.focus_force()  # 强制聚焦已有菜单
                    return  # 不重复创建菜单
            except tk.TclError:  # 捕获菜单窗口已失效的异常
                pass  # 准备清理失效菜单
            self.overlay._dismiss_tray_menu()  # 关闭失效或旧托盘菜单

        menu = tk.Toplevel(self.overlay.root)  # 创建菜单顶层窗口
        menu.withdraw()  # 初始隐藏菜单窗口
        menu.title("时间悬浮窗菜单")  # 设置菜单窗口标题
        menu.transient(self.overlay.root)  # 将菜单设为悬浮窗的临时窗口
        menu.overrideredirect(True)  # 移除系统标题栏和边框
        menu.attributes("-topmost", True)  # 始终将菜单置于顶层
        menu.configure(bg="#CACACAC5")  # 设置菜单背景颜色

        panel = tk.Frame(menu, bg="#CACACAC5", padx=6, pady=6)  # 创建菜单面板
        panel.pack(fill=tk.BOTH, expand=True)  # 填充整个菜单窗口

        def close_menu() -> None:  # 定义关闭托盘菜单函数
            self.overlay._dismiss_tray_menu()  # 调用悬浮窗的菜单关闭逻辑

        def invoke(action: str) -> None:  # 定义菜单动作执行函数
            close_menu()  # 先关闭托盘菜单
            self.action_queue.put(action)  # 将所选动作加入队列

        def add_item(  # 定义菜单项添加函数
            label: str,  # 接收菜单项文本
            action: str,  # 接收对应动作标识
            selected: bool = False,  # 指示菜单项是否已选中
            color: str | None = None,  # 接收可选文本颜色
        ) -> None:
            prefix = "✓  " if selected else "   "  # 根据选中状态生成前缀
            button = tk.Button(  # 创建菜单项按钮
                panel,  # 指定按钮父容器
                text=prefix + label,  # 设置按钮显示文本
                anchor=tk.W,  # 靠左对齐按钮文本
                command=lambda: invoke(action),  # 设置点击动作回调
                relief=tk.FLAT,  # 使用无边框按钮样式
                bd=0,  # 设置按钮边框宽度为零
                padx=8,  # 设置按钮横向内边距
                pady=3,  # 设置按钮纵向内边距
                bg="#CACACAC5",  # 设置按钮背景颜色
                activebackground="#A3A3A3",  # 设置鼠标悬停背景颜色
                fg=color or "#000000",  # 设置字体颜色
                activeforeground=color or "#000000",  # 设置悬停字体颜色
                font=(MENU_FONT_FAMILY, MENU_ITEM_FONT_SIZE, "bold"),  # 设置按钮字体
                cursor="arrow",  # 设置鼠标悬停光标
                highlightthickness=0,  # 隐藏按钮焦点高亮
            )
            button.pack(fill=tk.X)  # 将按钮按水平宽度填充面板
            button.bind(  # 为鼠标进入事件绑定处理
                "<Enter>", lambda _event: button.configure(bg="#B3B0B0")  # 鼠标悬停时更改背景色
            )
            button.bind(  # 为鼠标离开事件绑定处理
                "<Leave>", lambda _event: button.configure(bg="#CACACAC5")  # 鼠标离开时恢复背景色
            )

        def add_heading(label: str) -> None:  # 定义菜单标题添加函数
            tk.Label(  # 创建标题标签
                panel,  # 指定标签父容器
                text=label,  # 设置标题文本
                anchor=tk.W,  # 靠左对齐标题文本
                bg="#CACACAC5",  # 设置标题背景颜色
                fg="#000000",  # 设置标题字体颜色
                font=(MENU_FONT_FAMILY, MENU_HEADING_FONT_SIZE, "bold"),  # 设置标题字体
                padx=8,  # 设置标题横向内边距
                pady=3,  # 设置标题纵向内边距
            ).pack(fill=tk.X)  # 填充并显示标题标签

        def add_separator() -> None:  # 定义菜单分隔线添加函数
            tk.Frame(panel, bg="#AAAAAA", height=1).pack(  # 创建并显示分隔线框架
                fill=tk.X, padx=8, pady=3  # 设置水平填充与外边距
            )

        clock_label = "隐藏时钟" if self.overlay.clock_visible else "显示时钟"  # 根据时钟可见状态生成操作文本
        add_item(clock_label, "toggle_clock")  # 添加时钟显示切换菜单项
        add_separator()  # 添加分隔线

        add_heading("时间字号")  # 添加字号设置分组标题
        for index, size in enumerate(FONT_SIZE_PRESETS):  # 遍历预设字号
            add_item(  # 添加一个字号选项
                f"{size} 像素",  # 设置字号选项文本
                f"size:{size}",  # 设置字号动作标识
                selected=size == self.overlay.font_size,  # 标记当前选中字号
            )
        add_item("自定义字号...", "custom_size")  # 添加自定义字号菜单项

        add_separator()  # 添加分隔线
        add_heading("时间颜色")  # 添加颜色设置分组标题
        for name, color in COLOR_PRESETS:  # 遍历预设颜色
            add_item(  # 添加一个颜色选项
                name,  # 设置颜色名称
                f"color:{color}",  # 设置颜色动作标识
                selected=color.casefold()
                == self.overlay.clock_color.casefold(),  # 标记当前选中颜色
                color=color,  # 设置选项文本颜色
            )
        add_item("自定义颜色...", "custom_color")  # 添加自定义颜色菜单项

        add_separator()  # 添加分隔线
        add_item(  # 添加透明度菜单项
            f"透明度...（当前 {self.overlay.transparency}%）",  # 显示当前透明度
            "transparency",  # 设置透明度动作标识
        )
        add_item(  # 添加开机自启动菜单项
            ("✓  " if self.overlay.autostart_enabled else "   ")  # 根据状态生成选中前缀
            + "开机自启动",  # 拼接菜单项文本
            "toggle_autostart",  # 设置自启动切换动作标识
        )
        add_separator()  # 添加分隔线
        add_item("退出程序", "quit")  # 添加退出程序菜单项

        def close_if_focus_left(_event: tk.Event) -> None:  # 定义焦点离开菜单时的关闭逻辑
            def check_focus() -> None:  # 定义延迟检查焦点函数
                try:
                    focused = menu.focus_get()  # 获取当前焦点控件
                    if focused is None or focused.winfo_toplevel() is not menu:  # 判断焦点是否仍在菜单内
                        close_menu()  # 然后关闭菜单
                except tk.TclError:  # 捕获窗口失效异常
                    close_menu()  # 确保失效窗口仍会关闭

            menu.after(100, check_focus)  # 延迟检查菜单焦点状态

        menu.bind("<Escape>", lambda _event: close_menu())  # 按下 Escape 键时关闭菜单
        menu.bind("<FocusOut>", close_if_focus_left)  # 焦点离开时安排菜单关闭检查
        menu.update_idletasks()  # 立即更新菜单控件布局状态

        cursor = POINT()  # 创建鼠标位置结构
        if not self.user32.GetCursorPos(ctypes.byref(cursor)):  # 获取鼠标屏幕坐标
            menu.destroy()  # 获取失败时销毁菜单窗口
            raise ctypes.WinError(ctypes.get_last_error())  # 抛出坐标获取失败错误
        width = menu.winfo_reqwidth()  # 获取菜单所需宽度
        height = menu.winfo_reqheight()  # 获取菜单所需高度
        x, y = tray_menu_position(  # 计算适合托盘位置的菜单坐标
            cursor.x,  # 传入鼠标横坐标
            cursor.y,  # 传入鼠标纵坐标
            width,  # 传入菜单宽度
            height,  # 传入菜单高度
            self.overlay._virtual_screen_bounds(),  # 传入虚拟屏幕边界
        )
        menu.geometry(f"+{x}+{y}")  # 将菜单移动到计算出的坐标
        menu.deiconify()  # 显示菜单窗口
        menu.lift()  # 将菜单置于窗口前台
        menu.focus_force()  # 强制聚焦菜单窗口
        self.overlay.tray_menu = menu  # 保存当前托盘菜单对象
        menu.update_idletasks()  # 更新菜单布局以取得准确尺寸
        self.overlay.tray_menu_bounds = (  # 记录菜单在屏幕上的边界
            menu.winfo_rootx(),  # 记录菜单左侧坐标
            menu.winfo_rooty(),  # 记录菜单顶部坐标
            menu.winfo_rootx() + menu.winfo_width(),  # 记录菜单右侧坐标
            menu.winfo_rooty() + menu.winfo_height(),  # 记录菜单底部坐标
        )
        self.overlay.tray_menu_dismiss_queued = False  # 清除菜单关闭排队标记
        try:
            self.overlay._install_mouse_hook()  # 安装全局鼠标钩子以监听菜单外点击
        except OSError:  # 捕获鼠标钩子安装异常
            self.overlay._dismiss_tray_menu()  # 安装失败时关闭菜单
            raise  # 保留原始异常供上层处理
        schedule_rounded_corners(menu)  # 为菜单窗口安排圆角效果

    def close(self) -> None:  # 定义托盘资源清理函数
        if self.hwnd:  # 判断托盘窗口是否存在
            self.shell32.Shell_NotifyIconW(  # 删除系统托盘图标
                NIM_DELETE, ctypes.byref(self.icon_data)  # 指定删除操作及图标数据
            )
            self.user32.DestroyWindow(self.hwnd)  # 销毁托盘消息窗口
            self.user32.UnregisterClassW(self.class_name, self.instance)  # 注销托盘窗口类
            self.user32.DestroyIcon(self.icon_data.hIcon)  # 销毁托盘图标资源
            self.hwnd = None  # 清空托盘窗口句柄


def main() -> int:
    if os.name != "nt":
        print("This overlay requires Windows.", file=sys.stderr)
        return 1

    mutex = acquire_single_instance_mutex()
    if mutex is None:
        return 0
    try:
        enable_high_dpi_awareness()
        root = tk.Tk()
        try:
            TimeOverlay(root)
        except (OSError, ValueError) as error:
            root.destroy()
            messagebox.showerror(APP_PUBLISHER, str(error))
            return 1

        root.mainloop()
        return 0
    finally:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        kernel32.CloseHandle.restype = wintypes.BOOL
        if not kernel32.CloseHandle(mutex):
            raise ctypes.WinError(ctypes.get_last_error())


if __name__ == "__main__":
    raise SystemExit(main())
