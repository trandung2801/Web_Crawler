import json
import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from download_image import download_image

# Logging
logging.basicConfig(filename = 'app.log', filemode = 'w', format = '%(name)s - %(levelname)s - %(message)s')


# Class implement multiple thread
class CrawlProduct():
    GROUP_PRODUCTS = ["Apple", "Samsung", "Xiaomi", "OPPO", "Nokia", "Realme", "Vsmart", "ASUS", "Vivo", "OnePlus",
                      "POCOPhone", "Nubia"]
    
    

    index = 1
    ids = []

    def __init__(self, data):
        self.data = data

    def crawl(self):
        for group in self.GROUP_PRODUCTS:
            # Chrome driver
            # driver = webdriver.Chrome("C:/Windows/chromedriver.exe")
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get("https://cellphones.com.vn/mobile/" + group + ".html")

            content = driver.page_source
            soup = BeautifulSoup(content)

            try:
                # show_more = driver.find_element_by_css_selector('a.btn-show-more.btn-load-more')
                show_more = driver.find_elements_by_class_name('button btn-show-more button__show-more-product')
                # Show more all page
                while show_more.get_attribute("style") != "display: none;":
                    driver.execute_script("document.getElementsByClassName('button btn-show-more button__show-more-product')[0].click();")
                    time.sleep(4)
                # Get page source again after show more
                content = driver.page_source
                soup = BeautifulSoup(content)
            except:
                logging.info(group + " can't show more")

            # List all item product
            list_product = soup.find_all("div", attrs = {"class", "product-info-container product-item"})

            # For each item in list product
            for item_product in list_product:
                _id = item_product.get("id")
                if _id not in self.ids:
                    product_name = item_product.find("div", attrs = {"class", "item-product__box-name"}).find("a")
                    link_product_detail = item_product.find("div", attrs = {"class", "item-product__box-img"}) \
                        .find("a").get("href")
                    img_src = item_product.find("div", attrs = {"class", "item-product__box-img"}).find("img").get(
                        "src")
                    img_name = _id + ".jpg"
                    old_price = item_product.find("div", attrs = {"class", "item-product__box-price"}) \
                        .find("p", attrs = {"class", "old-price"})
                    special_price = item_product.find("div", attrs = {"class", "item-product__box-price"}) \
                        .find("p", attrs = {"class", "special-price"})
                    self.ids.append(_id)
                    # Download image
                    try:
                        download_image(img_src, img_name)
                        time.sleep(2)
                    except:
                        logging.warning(f"Product {_id} download failed")
                        img_name = ""

                    if old_price is not None:
                        # Format price (str) to float:  32.990.000 ₫ --> 32990000
                        format_price = old_price.text.translate({ord(i): None for i in ' .₫'})
                        old_price = float(format_price)
                    else:
                        old_price = None
                    if special_price is not None and not "Đăng ký nhận tin":
                        format_price = special_price.text.translate({ord(i): None for i in ' .₫'})
                        special_price = float(format_price)
                    else:
                        special_price = None

                    # Access to product detail page
                    driver.get(link_product_detail)
                    time.sleep(2)
                    # Get blog content & technical info
                    detail_content = driver.page_source
                    detail_soup = BeautifulSoup(detail_content)
                    div_blog_content = detail_soup.find("div", attrs = {"class", "blog-content"})
                    blog_content = "".join(str(item) for item in div_blog_content.contents)

                    parameter = []
                    for tr in detail_soup.select("#tskt tr"):
                        th = tr.select("th")
                        if th[0].text == "Hệ thống đang cập nhật ...":
                            break
                        parameter.append({"title": th[0].text, "parameter": th[1].text})

                    product = {
                        "id": _id,
                        "product_name": product_name.text,
                        "group": group,
                        "old_price": old_price,
                        "special_price": special_price,
                        "img_name": img_name,
                        "img_src": img_src,
                        "blog_content": blog_content,
                        "parameters": parameter
                    }

                    self.data["mobile"].append(product)
            # Quit selenium
            driver.quit()


data = {"mobile": []}
run = CrawlProduct(data)
run.crawl()

# Export to .json
with open("product_mobile.json", 'a+', encoding = "utf8") as outfile:
    json.dump(data, outfile, ensure_ascii = False, indent = 4)

print("done !")
