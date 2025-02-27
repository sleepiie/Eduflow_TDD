import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):  
    def setUp(self):  
        self.browser = webdriver.Chrome()  

    def tearDown(self):  
        self.browser.quit()

    def test_can_start_homepage(self):  

        #แทนเจอเว็บ “EduFlow” เป็นเว็บสำหรับวางแผนเวลาเกี่ยวกับการเรียน แทนเลยกดเข้าเว็บ
        self.browser.get("http://localhost:8000")  

        #หน้าเว็บแสดงหน้าหลัก โดยมี title เขียนว่า Eduflow  
        self.assertIn("EduFlow", self.browser.title) 
            ##และมีข้อความเขียนว่า Eduflow ในหน้าหลัก
        header = self.browser.find_element(By.ID, "header")
        self.assertIn("Eduflow", header)
            ##และมีปุ่ม "Create Categories"
        create_categories_btn = self.browser.find_element(By.ID , "create_categories").text
        self.assertIn("Create Categories" , create_categories_btn)

    
        self.fail("Finish the test!")  


if __name__ == "__main__":  
    unittest.main()  