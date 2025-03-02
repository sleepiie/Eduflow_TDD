from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase


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
