"""
By 叫我杨同学 in bilibili
2026-4-18
EasyClass 1.0.0
Build by nuitka onefile mode
Open in github
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from PIL import Image, ImageDraw, ImageFont

class CourseScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("课程表管理系统")
        self.root.geometry("1000x600")
        
        # 课程数据
        self.courses = []
        self.data_file = "courses.json"
        
        # 浮窗相关
        self.floating_window = None
        self.floating_timer = None
        
        # 加载数据
        self.load_data()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部按钮栏
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        self.add_button = ttk.Button(self.button_frame, text="添加课程", command=self.add_course)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(self.button_frame, text="编辑课程", command=self.edit_course)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(self.button_frame, text="删除课程", command=self.delete_course)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.export_calendar_button = ttk.Button(self.button_frame, text="导出日历", command=self.export_calendar)
        self.export_calendar_button.pack(side=tk.LEFT, padx=5)
        
        self.export_image_button = ttk.Button(self.button_frame, text="导出图片", command=self.export_image)
        self.export_image_button.pack(side=tk.LEFT, padx=5)
        
        self.import_calendar_button = ttk.Button(self.button_frame, text="导入日历", command=self.import_calendar)
        self.import_calendar_button.pack(side=tk.LEFT, padx=5)
        
        self.show_floating_button = ttk.Button(self.button_frame, text="显示浮窗", command=self.show_floating_window)
        self.show_floating_button.pack(side=tk.LEFT, padx=5)
        
        self.hide_floating_button = ttk.Button(self.button_frame, text="隐藏浮窗", command=self.hide_floating_window)
        self.hide_floating_button.pack(side=tk.LEFT, padx=5)
        
        # 创建课程表框架
        self.schedule_frame = ttk.LabelFrame(self.main_frame, text="课程表", padding="10")
        self.schedule_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建课程表表格
        self.create_schedule_table()
    
    def create_schedule_table(self):
        # 星期几
        weekdays = ["周一", "周二", "周三", "周四", "周五"]
        # 节次
        sections = ["第1节", "第2节", "第3节", "第4节", "第5节", "第6节", "第7节", "第8节"]
        
        # 创建表格
        self.table_frame = ttk.Frame(self.schedule_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        self.vscrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hscrollbar = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=["section"] + weekdays, show="headings",
                               yscrollcommand=self.vscrollbar.set, xscrollcommand=self.hscrollbar.set)
        
        self.vscrollbar.config(command=self.tree.yview)
        self.hscrollbar.config(command=self.tree.xview)
        
        # 设置列标题
        self.tree.heading("section", text="节次")
        for day in weekdays:
            self.tree.heading(day, text=day)
        
        # 设置列宽
        self.tree.column("section", width=80)
        for day in weekdays:
            self.tree.column(day, width=120)
        
        # 填充数据
        for i, section in enumerate(sections):
            values = [section]
            for day in range(7):
                # 查找该节次的课程
                course_info = ""
                for course in self.courses:
                    if course["weekday"] == day and course["section"] == i + 1:
                        course_info = f"{course['name']}\n{course['classroom']}"
                        break
                values.append(course_info)
            self.tree.insert("", tk.END, values=values)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def add_course(self):
        self.course_dialog("添加课程")
    
    def edit_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要编辑的课程")
            return
        
        # 获取选择的行
        item = selected_item[0]
        values = self.tree.item(item, "values")
        section_index = int(values[0].replace("第", "").replace("节", "")) - 1
        
        # 显示课程选择对话框
        course_options = []
        for course in self.courses:
            if course["section"] == section_index + 1:
                weekday_name = ["周一", "周二", "周三", "周四", "周五"][course["weekday"]]
                course_options.append(f"{weekday_name} - {course['name']} ({course['classroom']})")
        
        if not course_options:
            messagebox.showinfo("提示", "未找到该节次的课程")
            return
        
        # 创建选择对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("选择课程")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="请选择要编辑的课程:").pack(pady=10)
        
        # 创建列表框
        listbox = tk.Listbox(dialog, width=50, height=10)
        for option in course_options:
            listbox.insert(tk.END, option)
        listbox.pack(pady=10, padx=10)
        listbox.select_set(0)  # 默认选择第一个
        
        # 按钮
        def select_course():
            selected_index = listbox.curselection()
            if selected_index:
                # 查找对应的课程
                target_course = None
                for course in self.courses:
                    if course["section"] == section_index + 1:
                        weekday_name = ["周一", "周二", "周三", "周四", "周五"][course["weekday"]]
                        course_text = f"{weekday_name} - {course['name']} ({course['classroom']})"
                        if course_text == course_options[selected_index[0]]:
                            target_course = course
                            break
                
                if target_course:
                    dialog.destroy()
                    self.course_dialog("编辑课程", target_course)
            else:
                messagebox.showinfo("提示", "请选择要编辑的课程")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="确定", command=select_course).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def delete_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要删除的课程")
            return
        
        # 获取选择的行
        item = selected_item[0]
        values = self.tree.item(item, "values")
        section_index = int(values[0].replace("第", "").replace("节", "")) - 1
        
        # 显示课程选择对话框
        course_options = []
        for course in self.courses:
            if course["section"] == section_index + 1:
                weekday_name = ["周一", "周二", "周三", "周四", "周五"][course["weekday"]]
                course_options.append(f"{weekday_name} - {course['name']} ({course['classroom']})")
        
        if not course_options:
            messagebox.showinfo("提示", "未找到该节次的课程")
            return
        
        # 创建选择对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("选择课程")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="请选择要删除的课程:").pack(pady=10)
        
        # 创建列表框
        listbox = tk.Listbox(dialog, width=50, height=10)
        for option in course_options:
            listbox.insert(tk.END, option)
        listbox.pack(pady=10, padx=10)
        listbox.select_set(0)  # 默认选择第一个
        
        # 按钮
        def select_course():
            selected_index = listbox.curselection()
            if selected_index:
                # 查找对应的课程
                target_course = None
                for course in self.courses:
                    if course["section"] == section_index + 1:
                        weekday_name = ["周一", "周二", "周三", "周四", "周五"][course["weekday"]]
                        course_text = f"{weekday_name} - {course['name']} ({course['classroom']})"
                        if course_text == course_options[selected_index[0]]:
                            target_course = course
                            break
                
                if target_course:
                    # 确认删除
                    if messagebox.askyesno("确认删除", f"确定要删除课程 {target_course['name']} 吗？"):
                        self.courses.remove(target_course)
                        self.save_data()
                        self.refresh_schedule()
                        messagebox.showinfo("成功", "课程已删除")
                    dialog.destroy()
            else:
                messagebox.showinfo("提示", "请选择要删除的课程")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="确定", command=select_course).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def course_dialog(self, title, course=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 预设课程列表
        preset_courses = [
            "语文", "数学", "英语", "物理", "化学", "生物", "历史", "地理", "政治", "音乐", "美术", "体育", "信息技术"
        ]
        
        # 创建表单
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # 预设课程
        ttk.Label(form_frame, text="预设课程:").grid(row=0, column=0, sticky=tk.W, pady=5)
        preset_var = tk.StringVar()
        preset_combo = ttk.Combobox(form_frame, textvariable=preset_var, values=["自定义"] + preset_courses, width=28)
        preset_combo.grid(row=0, column=1, pady=5)
        preset_combo.current(0)
        
        # 预设课程选择事件
        def on_preset_select(event):
            selected_preset = preset_var.get()
            if selected_preset != "自定义":
                name_var.set(selected_preset)
        
        preset_combo.bind("<<ComboboxSelected>>", on_preset_select)
        
        # 课程名称
        ttk.Label(form_frame, text="课程名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=30).grid(row=1, column=1, pady=5)
        
        # 教师
        ttk.Label(form_frame, text="教师:").grid(row=2, column=0, sticky=tk.W, pady=5)
        teacher_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=teacher_var, width=30).grid(row=2, column=1, pady=5)
        
        # 星期几
        ttk.Label(form_frame, text="星期几:").grid(row=3, column=0, sticky=tk.W, pady=5)
        weekday_var = tk.StringVar()
        weekday_combo = ttk.Combobox(form_frame, textvariable=weekday_var, values=["周一", "周二", "周三", "周四", "周五"], width=28)
        weekday_combo.grid(row=3, column=1, pady=5)
        weekday_combo.current(0)
        
        # 第几节
        ttk.Label(form_frame, text="第几节:").grid(row=4, column=0, sticky=tk.W, pady=5)
        section_var = tk.StringVar()
        section_combo = ttk.Combobox(form_frame, textvariable=section_var, values=["1", "2", "3", "4", "5", "6", "7", "8"], width=28)
        section_combo.grid(row=4, column=1, pady=5)
        section_combo.current(0)
        
        # 开始时间
        ttk.Label(form_frame, text="开始时间:").grid(row=5, column=0, sticky=tk.W, pady=5)
        start_time_var = tk.StringVar(value="08:00")
        ttk.Entry(form_frame, textvariable=start_time_var, width=30).grid(row=5, column=1, pady=5)
        
        # 结束时间
        ttk.Label(form_frame, text="结束时间:").grid(row=6, column=0, sticky=tk.W, pady=5)
        end_time_var = tk.StringVar(value="08:45")
        ttk.Entry(form_frame, textvariable=end_time_var, width=30).grid(row=6, column=1, pady=5)
        
        # 教室
        ttk.Label(form_frame, text="教室:").grid(row=7, column=0, sticky=tk.W, pady=5)
        classroom_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=classroom_var, width=30).grid(row=7, column=1, pady=5)
        
        # 单双周
        ttk.Label(form_frame, text="单双周:").grid(row=8, column=0, sticky=tk.W, pady=5)
        week_type_var = tk.StringVar()
        week_type_combo = ttk.Combobox(form_frame, textvariable=week_type_var, values=["所有周", "单周", "双周"], width=28)
        week_type_combo.grid(row=8, column=1, pady=5)
        week_type_combo.current(0)
        
        # 如果是编辑模式，预填充表单
        if course:
            name_var.set(course["name"])
            teacher_var.set(course["teacher"])
            weekdays = ["周一", "周二", "周三", "周四", "周五"]
            weekday_var.set(weekdays[course["weekday"]])
            section_var.set(str(course["section"]))
            start_time_var.set(course["start_time"])
            end_time_var.set(course["end_time"])
            classroom_var.set(course["classroom"])
            week_type_var.set(course["week_type"])
        
        # 按钮
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=10)
        
        def save_course():
            course_data = {
                "name": name_var.get(),
                "teacher": teacher_var.get(),
                "weekday": ["周一", "周二", "周三", "周四", "周五"].index(weekday_var.get()),
                "section": int(section_var.get()),
                "start_time": start_time_var.get(),
                "end_time": end_time_var.get(),
                "classroom": classroom_var.get(),
                "week_type": week_type_var.get()
            }
            
            if not course_data["name"]:
                messagebox.showerror("错误", "课程名称不能为空")
                return
            
            # 检查是否与现有课程重复
            if not course:
                for existing_course in self.courses:
                    if (existing_course["weekday"] == course_data["weekday"] and
                        existing_course["section"] == course_data["section"]):
                        # 发现重复课程
                        response = messagebox.askyesno(
                            "课程重复",
                            f"在 {['周一', '周二', '周三', '周四', '周五'][course_data['weekday']]} 第{course_data['section']}节已有课程:\n" +
                            f"现有课程: {existing_course['name']}\n" +
                            f"新课程: {course_data['name']}\n\n" +
                            "是否替换现有课程？"
                        )
                        if response:
                            # 替换现有课程
                            self.courses.remove(existing_course)
                            self.courses.append(course_data)
                        else:
                            # 取消添加
                            return
            
            if course:
                # 编辑模式：更新现有课程
                index = self.courses.index(course)
                self.courses[index] = course_data
            else:
                # 添加模式：添加新课程
                self.courses.append(course_data)
            
            self.save_data()
            self.refresh_schedule()
            dialog.destroy()
        
        ttk.Button(button_frame, text="保存", command=save_course).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def refresh_schedule(self):
        # 清除现有表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 重新填充数据
        sections = ["第1节", "第2节", "第3节", "第4节", "第5节", "第6节", "第7节", "第8节"]
        weekdays = ["周一", "周二", "周三", "周四", "周五"]
        
        for i, section in enumerate(sections):
            values = [section]
            for day in range(5):  # 只显示周一到周五
                # 查找该节次的课程
                course_info = ""
                for course in self.courses:
                    if course["weekday"] == day and course["section"] == i + 1:
                        course_info = f"{course['name']}\n{course['classroom']}"
                        break
                values.append(course_info)
            self.tree.insert("", tk.END, values=values)
    
    def save_data(self):
        try:
            # 确保数据文件所在目录存在
            data_dir = os.path.dirname(self.data_file)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # 检查路径是否是目录
            if os.path.isdir(self.data_file):
                messagebox.showerror("错误", f"保存失败：{self.data_file} 是一个文件夹，不是文件！\n请检查程序配置。")
                return
            
            # 尝试创建备份文件
            backup_file = self.data_file + ".bak"
            if os.path.exists(self.data_file):
                try:
                    with open(self.data_file, "r", encoding="utf-8") as f:
                        backup_data = f.read()
                    with open(backup_file, "w", encoding="utf-8") as f:
                        f.write(backup_data)
                except:
                    pass  # 备份失败不影响主流程
            
            # 保存数据
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.courses, f, ensure_ascii=False, indent=2)
        except PermissionError:
            error_msg = f"没有权限写入文件: {self.data_file}\n\n请检查：\n1. 文件是否被其他程序打开（如Excel、记事本、VS Code）\n2. 是否以管理员身份运行程序\n3. 文件是否是只读属性"
            messagebox.showerror("权限不足", error_msg)
        except IsADirectoryError:
            messagebox.showerror("错误", f"错误：{self.data_file} 是一个文件夹，不能直接写入！")
        except FileNotFoundError:
            messagebox.showerror("错误", f"文件不存在或路径错误: {self.data_file}\n请检查程序配置。")
        except IOError as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"保存数据时发生错误: {str(e)}")
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.courses = json.load(f)
            except:
                self.courses = []
    
    def export_calendar(self):
        if not self.courses:
            messagebox.showerror("错误", "没有课程数据可导出")
            return
        
        # 创建日历
        cal = Calendar()
        cal.add('prodid', '-//Course Scheduler//Course Calendar//CN')
        cal.add('version', '2.0')
        
        # 添加课程事件
        for course in self.courses:
            event = Event()
            event.add('summary', course['name'])
            event.add('description', f"教师: {course['teacher']}\n教室: {course['classroom']}\n节次: {course['section']}\n{course['week_type']}")
            event.add('location', course['classroom'])
            
            # 设置时间
            start_hour, start_minute = map(int, course['start_time'].split(':'))
            end_hour, end_minute = map(int, course['end_time'].split(':'))
            
            # 以当前周为基准
            today = datetime.now()
            # 计算本周一的日期
            monday = today - timedelta(days=today.weekday())
            # 计算课程日期
            course_date = monday + timedelta(days=course['weekday'])
            
            start_time = course_date.replace(hour=start_hour, minute=start_minute)
            end_time = course_date.replace(hour=end_hour, minute=end_minute)
            
            event.add('dtstart', start_time)
            event.add('dtend', end_time)
            event.add('dtstamp', datetime.now())
            
            # 添加重复规则 (每周重复)
            rrule = {'FREQ': 'WEEKLY'}
            # 处理单双周
            if course['week_type'] == '单周':
                rrule['INTERVAL'] = 2
                rrule['BYSETPOS'] = 1  # 单周
            elif course['week_type'] == '双周':
                rrule['INTERVAL'] = 2
                rrule['BYSETPOS'] = 2  # 双周
            event.add('rrule', rrule)
            
            # 添加到日历
            cal.add_component(event)
        
        # 保存文件
        file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")])
        if file_path:
            with open(file_path, 'wb') as f:
                f.write(cal.to_ical())
            messagebox.showinfo("成功", f"日历已导出到: {file_path}")
    
    def export_image(self):
        if not self.courses:
            messagebox.showerror("错误", "没有课程数据可导出")
            return
        
        # 创建图片
        width, height = 1000, 800
        #2 8023 38
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # 尝试加载字体
        try:
            font = ImageFont.truetype('simhei.ttf', 16)
            title_font = ImageFont.truetype('simhei.ttf', 24)
        except:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()
        
        # 计算表格居中偏移
        cell_width = width // 8
        table_width = 6 * cell_width  # 节次 + 周一到周五
        offset_x = (width - table_width) // 2  # 水平居中偏移
        
        # 绘制标题
        draw.text((width//2, 30), "课程表", fill='black', font=title_font, anchor='mm')
        
        # 绘制表格
        cell_height = (height - 100) // 9
        
        # 绘制表头
        weekdays = ["节次", "周一", "周二", "周三", "周四", "周五"]
        for i, day in enumerate(weekdays):
            x = offset_x + i * cell_width
            y = 80
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline='black')
            draw.text((x + cell_width//2, y + cell_height//2), day, fill='black', font=font, anchor='mm')
        
        # 绘制节次和课程
        sections = ["第1节", "第2节", "第3节", "第4节", "第5节", "第6节", "第7节", "第8节"]
        for i, section in enumerate(sections):
            # 绘制节次
            x = offset_x
            y = 80 + (i + 1) * cell_height
            draw.rectangle([x, y, x + cell_width, y + cell_height], outline='black')
            draw.text((x + cell_width//2, y + cell_height//2), section, fill='black', font=font, anchor='mm')
            
            # 绘制课程
            for day in range(5):  # 周一到周五
                x = offset_x + (day + 1) * cell_width
                draw.rectangle([x, y, x + cell_width, y + cell_height], outline='black')
                
                # 查找课程
                course_info = ""
                for course in self.courses:
                    if course["weekday"] == day and course["section"] == i + 1:
                        course_info = f"{course['name']}\n{course['classroom']}"
                        break
                
                # 绘制课程信息
                if course_info:
                    lines = course_info.split('\n')
                    # 计算垂直居中位置
                    line_height = 20
                    total_height = len(lines) * line_height
                    start_y = y + (cell_height - total_height) // 2
                    
                    for j, line in enumerate(lines):
                        draw.text((x + cell_width//2, start_y + j * line_height), line, fill='black', font=font, anchor='mm')
        
        # 保存图片
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            image.save(file_path)
            messagebox.showinfo("成功", f"课程表图片已保存到: {file_path}")
    
    def import_calendar(self):
        # 选择.ics文件
        file_path = filedialog.askopenfilename(filetypes=[("iCalendar files", "*.ics")])
        if not file_path:
            return
        
        try:
            # 读取并解析.ics文件
            with open(file_path, 'rb') as f:
                cal = Calendar.from_ical(f.read())
            
            # 提取事件
            imported_courses = []
            # 用于检测导入文件内部的冲突
            imported_slots = set()
            
            for component in cal.walk():
                if component.name == 'VEVENT':
                    # 提取事件信息
                    summary = str(component.get('summary', ''))
                    description = str(component.get('description', ''))
                    location = str(component.get('location', ''))
                    start = component.get('dtstart')
                    end = component.get('dtend')
                    
                    if start and end:
                        # 处理时间
                        start_time = start.dt
                        end_time = end.dt
                        
                        # 确保时间是本地时间
                        if not hasattr(start_time, 'tzinfo') or start_time.tzinfo is None:
                            # 无时区信息，按本地时间处理
                            import time
                            # 转换为本地时间
                            start_time = start_time.replace(tzinfo=None)
                            end_time = end_time.replace(tzinfo=None)
                        
                        # 获取星期几（0-6，0是周一）
                        weekday = start_time.weekday()
                        
                        # 计算节次（优先从描述中提取）
                        section = 1
                        
                        # 尝试从描述中提取节次信息
                        if description:
                            lines = description.split('\n')
                            for line in lines:
                                if '节次:' in line:
                                    try:
                                        section = int(line.replace('节次:', '').strip())
                                        break
                                    except:
                                        pass
                        
                        # 如果没有提取到节次，根据时间计算
                        if section == 1:
                            hour = start_time.hour
                            minute = start_time.minute
                            
                            # 根据具体的开始时间计算节次
                            # 与课程表的默认时间设置保持一致
                            if (hour == 8 and minute < 45):
                                section = 1
                            elif (hour == 8 and minute >= 45) or (hour == 9 and minute < 30):
                                section = 2
                            elif (hour == 9 and minute >= 30) or (hour == 10 and minute < 15):
                                section = 3
                            elif (hour == 10 and minute >= 15) or (hour == 11 and minute < 0):
                                section = 4
                            elif (hour == 11 and minute < 45):
                                section = 5
                            elif (hour == 14 and minute < 45):
                                section = 6
                            elif (hour == 14 and minute >= 45) or (hour == 15 and minute < 30):
                                section = 7
                            elif (hour == 15 and minute >= 30) or (hour == 16 and minute < 15):
                                section = 8
                        
                        # 只导入周一到周五的课程
                        if weekday > 4:  # 0-4是周一到周五
                            continue
                        
                        # 检查导入文件内部是否有冲突
                        slot_key = (weekday, section)
                        if slot_key in imported_slots:
                            print(f"跳过重复课程: {summary} (周{weekday+1}第{section}节)")
                            continue
                        imported_slots.add(slot_key)
                        
                        # 构建课程数据
                        course = {
                            "name": summary,
                            "teacher": "",  # 从描述中提取教师信息
                            "weekday": weekday,
                            "section": section,
                            "start_time": start_time.strftime("%H:%M"),
                            "end_time": end_time.strftime("%H:%M"),
                            "classroom": location,
                            "week_type": "所有周"
                        }
                        
                        # 尝试从描述中提取教师信息
                        if description:
                            lines = description.split('\n')
                            for line in lines:
                                if '教师:' in line:
                                    course['teacher'] = line.replace('教师:', '').strip()
                                elif '单双周:' in line:
                                    course['week_type'] = line.replace('单双周:', '').strip()
                        
                        imported_courses.append(course)
            

            
            if not imported_courses:
                messagebox.showinfo("提示", "未从日历文件中找到课程信息")
                return
            
            # 处理重复课程
            new_courses = []
            updated_courses = []
            # 复制当前课程列表，避免在循环中修改导致的问题
            current_courses = self.courses.copy()
            
            for imported_course in imported_courses:
                # 检查是否与现有课程冲突
                conflict = False
                for i, existing_course in enumerate(current_courses):
                    if (existing_course["weekday"] == imported_course["weekday"] and
                        existing_course["section"] == imported_course["section"]):
                        # 冲突，询问用户如何处理
                        response = messagebox.askyesnocancel(
                            "课程冲突",
                            f"在 {['周一', '周二', '周三', '周四', '周五', '周六', '周日'][imported_course['weekday']]} 第{imported_course['section']}节已有课程:\n" +
                            f"现有课程: {existing_course['name']}\n" +
                            f"导入课程: {imported_course['name']}\n\n" +
                            "是否替换现有课程？\n" +
                            "是: 替换现有课程\n" +
                            "否: 保留现有课程\n" +
                            "取消: 取消导入"
                        )
                        
                        if response is None:
                            # 取消导入
                            return
                        elif response:
                            # 替换现有课程
                            current_courses[i] = imported_course
                            updated_courses.append(imported_course)
                        # 否则保留现有课程
                        conflict = True
                        break
                
                if not conflict:
                    # 无冲突，添加新课程
                    current_courses.append(imported_course)
                    new_courses.append(imported_course)
            
            # 更新课程列表
            self.courses = current_courses
            
            # 保存数据并刷新课程表
            self.save_data()
            self.refresh_schedule()
            
            # 显示导入结果
            message = f"导入完成！\n"
            if new_courses:
                message += f"新增课程: {len(new_courses)}\n"
            if updated_courses:
                message += f"更新课程: {len(updated_courses)}\n"
            message += f"总计处理: {len(imported_courses)} 个事件"
            messagebox.showinfo("成功", message)
            
        except Exception as e:
            messagebox.showerror("错误", f"导入日历失败: {str(e)}")
    
    def show_floating_window(self):
        if not self.floating_window:
            self.create_floating_window()
        else:
            self.floating_window.deiconify()
        self.start_floating_timer()
    
    def hide_floating_window(self):
        if self.floating_window:
            self.floating_window.withdraw()
        self.stop_floating_timer()
    
    def create_floating_window(self):
        self.floating_window = tk.Toplevel(self.root)
        self.floating_window.geometry("320x220")
        self.floating_window.attributes("-topmost", True)
        self.floating_window.overrideredirect(True)  # 隐藏窗口标题栏
        
        # 创建标签
        self.floating_label = ttk.Label(self.floating_window, text="", font=("SimHei", 12), justify=tk.LEFT, padding=10)
        self.floating_label.pack(fill=tk.BOTH, expand=True)
        
        # 添加关闭按钮
        close_button = ttk.Button(self.floating_window, text="×", width=3, command=self.hide_floating_window)
        close_button.place(x=270, y=5)
    
    def start_floating_timer(self):
        self.stop_floating_timer()
        self.update_floating_window()
        self.floating_timer = self.root.after(1000, self.start_floating_timer)  # 每秒更新一次
    
    def stop_floating_timer(self):
        if self.floating_timer:
            self.root.after_cancel(self.floating_timer)
            self.floating_timer = None
    
    def update_floating_window(self):
        if not self.floating_window or not self.floating_window.winfo_exists():
            return
        
        # 获取当前时间
        now = datetime.now()
        current_weekday = now.weekday()  # 0-6，0是周一，5是周六，6是周日
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")
        
        # 判断是否周末
        if current_weekday >= 5:
            content = f"当前时间: {current_date} 周末\n\n"
            content += "状态: 休息日\n"
            content += "今天无课"
            self.floating_label.config(text=content)
            return
        
        weekday_names = ["周一", "周二", "周三", "周四", "周五"]
        current_weekday_name = weekday_names[current_weekday]
        
        # 查找当前课程
        current_course = None
        for course in self.courses:
            if course["weekday"] == current_weekday:
                # 检查时间是否在课程时间范围内
                start_time = course["start_time"]
                end_time = course["end_time"]
                if start_time <= current_time[:5] < end_time:
                    current_course = course
                    break
        
        # 更新浮窗内容
        if current_course:
            # 计算下课剩余时间
            end_hour, end_minute = map(int, current_course["end_time"].split(":"))
            end_seconds = end_hour * 3600 + end_minute * 60
            now_seconds = now.hour * 3600 + now.minute * 60 + now.second
            remaining_seconds = end_seconds - now_seconds
            
            if remaining_seconds <= 0:
                remaining_text = "已下课"
            else:
                minutes, seconds = divmod(remaining_seconds, 60)
                remaining_text = f"{minutes}分{seconds}秒"
            
            content = f"当前时间: {current_date} {current_weekday_name} {current_time}\n\n"
            content += f"当前课程:\n"
            content += f"课程名称: {current_course['name']}\n"
            content += f"教师: {current_course['teacher']}\n"
            content += f"教室: {current_course['classroom']}\n"
            content += f"状态: 上课中\n"
            content += f"下课剩余: {remaining_text}"
        else:
            content = f"当前时间: {current_date} {current_weekday_name} {current_time}\n\n"
            content += "状态: 下课\n"
            content += "暂无课程"
        
        self.floating_label.config(text=content)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseScheduler(root)
    root.mainloop()