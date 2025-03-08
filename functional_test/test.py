from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from kanbanboard.models import Category , Topic


class NewVisitorTest(LiveServerTestCase):  
    def setUp(self):  
        self.browser = webdriver.Chrome()  

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_homepage(self):  

        #แทนเจอเว็บ “EduFlow” เป็นเว็บสำหรับวางแผนเวลาเกี่ยวกับการเรียน แทนเลยกดเข้าเว็บ
        self.browser.get(self.live_server_url)  

        #หน้าเว็บแสดงหน้าหลัก โดยมี title เขียนว่า Eduflow  
        self.assertIn("EduFlow", self.browser.title) 
            ##และมีข้อความเขียนว่า Eduflow ในหน้าหลัก
        header_text = self.browser.find_element(By.ID, "header").text
        self.assertIn("Eduflow", header_text)
            ##และมีปุ่ม "Create Categories"
        create_categories_btn = self.browser.find_element(By.ID , "create_categories").text
        self.assertIn("Create Categories" , create_categories_btn)
        
    def test_can_create_category(self):
        self.browser.get(self.live_server_url)  

        #แทนกดสร้างหมวดหมู่
        create_categories_btn = self.browser.find_element(By.ID , "create_categories")
        create_categories_btn.click()
        #หน้าเว็บแสดงป๊อปอัพให้ใส่ชื่อหมวดหมู่ที่ต้องการ
        alert = Alert(self.browser)

        #แทนใส่ชื่อบอร์ดว่า “Learn management”
        alert.send_keys("Learn management")
        alert.accept()

        #หน้าเว็บอัพเเดทและแสดงหมวดหมู่ขึ้นมาที่หน้าหลัก
        category_link = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Learn management"))
        )
        self.assertTrue(category_link.is_displayed())

    def test_can_create_topic(self):
        Category.objects.create(name="Learn management")

        self.browser.get(self.live_server_url)  
        #แทนกดเข้าไปในหมวดหมู่
        category_link = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Learn management"))
        )
        category_link.click()

        ###หน้าเว็บเปลี่ยนไปยังหน้า topic โดยมีชื่อ category อยู่ด้านบน
        header_text = self.browser.find_element(By.ID, "header").text
        self.assertIn("Learn management", header_text)

        #แทนเจอปุ่ม “Create Topic” แทนเลยลองกดปุ่ม “Create Topic”
        create_topic_btn = self.browser.find_element(By.ID , "create_topic").text
        self.assertIn("Create Topic" , create_topic_btn)
        #หน้าเว็บก็แสดงหน้าต่างสำหรับกรอกหัวข้อในหมวดหมู่นั้นขึ้นมา
        create_topic_btn = self.browser.find_element(By.ID , "create_topic")
        create_topic_btn.click()
        alert = Alert(self.browser)
        #แทนใส่ชื่อหัวข้อว่า “English”
        alert.send_keys("English")
        alert.accept()
        #หน้าเว็บอัพเดทและแสดง “English” ขึ้นมาในหมวดหมู่นั้น
        topic_link = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "English"))
        )
        self.assertTrue(topic_link.is_displayed())

    def test_can_create_and_manage_tasks(self):
        category = Category.objects.create(name="Learn management")
        topic = Topic.objects.create(category=category, name="English")
        
        #แทนกดเข้าไปในหัวข้อ English 
        self.browser.get(f"{self.live_server_url}/topic/{topic.id}/")
        #แทนเจอหน้า board ที่มี column todo, doing, done
        todo_column = self.browser.find_element(By.ID, "todo_column")
        doing_column = self.browser.find_element(By.ID, "doing_column")
        done_column = self.browser.find_element(By.ID, "done_column")
        
        self.assertTrue(todo_column.is_displayed())
        self.assertTrue(doing_column.is_displayed())
        self.assertTrue(done_column.is_displayed())
        
        #แทนเจอปุ่ม "add task" สำหรับเพิ่มข้อมูลลง board แทนลองกดเพิ่มข้อมูล
        add_task_btn = self.browser.find_element(By.ID, "add-task-btn")
        self.assertIn("Add Task", add_task_btn.text)
        add_task_btn.click()
        
        #หน้าเว็บแสดงป๊อปอัพสำหรับกรอกข้อมูลโดยมีให้กรอก title, due date และมีปุ่มสำหรับ save และ delete
        modal = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "task-modal"))
        )
        self.assertTrue(modal.is_displayed())
        
        #แทนกรอกข้อมูล title: อังกฤษ บท1, due date: 31-3-2025
        title_input = self.browser.find_element(By.ID, "task-title")
        due_date_input = self.browser.find_element(By.ID, "task-due-date")
        save_btn = self.browser.find_element(By.ID, "save-btn")
        
        title_input.send_keys("อังกฤษ บท1")
        due_date_input.send_keys("31-03-2025")
        
        #แทนกดปุ่ม save
        save_btn.click()
        
        #หน้าเว็บอัพเดทและแสดง task ที่แทนเขียนขึ้นมาบนหน้าเว็บ
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.ID, "task-modal"))
        )
        task = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'อังกฤษ บท1')]"))
        )
        self.assertTrue(task.is_displayed())
        
        due_date_text = self.browser.find_element(By.XPATH, "//div[contains(text(), '31-03-2025')]")
        self.assertTrue(due_date_text.is_displayed())
        
        #แทนต้องการแก้ไขข้อมูลใน task แทนจึงกดเข้าไปที่ task นั้นอีกครั้ง
        task.click()
        
        #หน้าเว็บแสดงป๊อปอัพสำหรับกรอกข้อมูลอีกครั้ง
        modal = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "task-modal"))
        )
        self.assertTrue(modal.is_displayed())
        
        #แทนแก้ไขข้อมูลเป็น due date: 4-4-2025
        due_date_input = self.browser.find_element(By.ID, "task-due-date")
        save_btn = self.browser.find_element(By.ID, "save-btn")

        due_date_input.clear()
        due_date_input.send_keys("04-04-2025")
        
        #แทนกดปุ่ม save
        save_btn.click()
        
        #หน้าเว็บทำการอัพเดท task ของแทนโดยวันที่จะเปลี่ยนจาก 31-3-2025 เป็น 4-4-2025
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.ID, "task-modal"))
        )
        
        updated_due_date = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '04-04-2025')]"))
        )
        self.assertTrue(updated_due_date.is_displayed())
        
        #แทนต้องการลบ task แทนเลยกดเข้าไปใน task นั้นอีกครั้ง
        task = self.browser.find_element(By.XPATH, "//div[contains(text(), 'อังกฤษ บท1')]")
        task.click()
        
        #แทนกดปุ่ม delete
        delete_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "delete-btn"))
        )
        delete_btn.click()

        alert = Alert(self.browser)
        alert.accept()
        
        #หน้าเว็บอัพเดท task หายไป
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(), 'อังกฤษ บท1')]"))
        )
        todo_tasks = self.browser.find_element(By.ID, "todo-tasks")
        self.assertNotIn("อังกฤษ บท1", todo_tasks.text)