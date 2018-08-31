from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import sys



def login_by_password(webdriver, username_xpath, user_name, password_xpath, password, login_btn_xpath):
    username_input = webdriver.find_element_by_xpath(username_xpath)
    username_input.send_keys(user_name)
    password_input = webdriver.find_element_by_xpath(password_xpath)
    password_input.send_keys(password)
    login_btn = webdriver.find_element_by_xpath(login_btn_xpath)
    login_btn.click()


def login(webdriver, url, login_xpath, username_xpath, user_name, password_xpath, password, login_btn_xpath):
    webdriver.get(url)
    if login_xpath is not None:
        login_btn = webdriver.find_element_by_xpath(login_xpath)
        login_btn.click()
        login_by_password(webdriver, username_xpath, user_name, password_xpath, password, login_btn_xpath)
    else:
        login_by_password(webdriver, username_xpath, user_name, password_xpath, password, login_btn_xpath)


def loginJueJin(webdriver, user_name, password, url='https://juejin.im/',
                login_xpath='//*[@id="juejin"]/div[2]/div/header/div/nav/ul/li[4]/span[1]',
                username_xpath='//*[@id="juejin"]/div[1]/div[3]/form/div[2]/div[1]/div[1]/input',
                password_xpath='//*[@id="juejin"]/div[1]/div[3]/form/div[2]/div[1]/div[2]/input',
                login_btn_xpath='//*[@id="juejin"]/div[1]/div[3]/form/div[2]/button'):
    login(webdriver, url, login_xpath, username_xpath, user_name, password_xpath, password, login_btn_xpath)


def wait_element_visible(webdriver, xpath, timeout=30):
    try:
        WebDriverWait(webdriver, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException as e:
        print("你的网络太渣了")


def wait_element_gone(webdriver, xpath, timeout=30):
    try:
        WebDriverWait(webdriver, timeout).until_not(ec.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException as e:
        print("这厮不消失")


def loginWeChat(webdriver, url='https://mp.weixin.qq.com/', login_xpath=None,
                username_xpath='//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input',
                username='wuhaoxuan1225@163.com',
                password_xpath='//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input',
                password='13223158738Wjx#',
                login_btn_xpath='//*[@id="header"]/div[2]/div/div/form/div[4]/a'):
    login(webdriver, url, login_xpath, username_xpath, username, password_xpath, password, login_btn_xpath)


def input_content(webdriver, title_xpath, title, content_xpath, content, *, is_wechat=False, author_xpath=None,
                  author=None):
    wait_element_visible(webdriver, title_xpath)
    title_input = webdriver.find_element_by_xpath(title_xpath)
    title_input.send_keys(title)
    # wait_element_visible(webdriver, content_xpath)
    content_input = webdriver.find_element_by_xpath(content_xpath)
    if is_wechat:
        content_input.send_keys(Keys.CONTROL, 'v')
    else:
        content = content.replace('"', '\\"').replace('\n', (' \\' + 'n ')).replace('\\"\\n\\"', '\\"\\\\n\\"')
        script = "arguments[0].value=\"%s\"" % content
        print('script is '+script)
        webdriver.execute_script(script, content_input)

    if is_wechat:
        author_input = webdriver.find_element_by_xpath('//*[@id="author"]')
        if author is not None:
            author_input.send_keys(author)
        # show original
        original_div = webdriver.find_element_by_xpath('//*[@id="js_article_url_area"]/label/label/span')
        webdriver.execute_script('arguments[0].scrollIntoView(true);', original_div)
        wait_element_visible(webdriver, '//*[@id="js_original"]/div[1]/div[2]/a')
        original_input = webdriver.find_element_by_xpath('//*[@id="js_original"]/div[1]/div[2]/a')
        webdriver.execute_script('arguments[0].click()', original_input)
        check_box_xpath = '/html/body/div[12]/div/div[2]/div[2]/div/div/div/div[2]/label/i'
        wait_element_visible(webdriver, check_box_xpath)
        check_box = webdriver.find_element_by_xpath(check_box_xpath)
        check_box.click()
        next_btn = webdriver.find_element_by_xpath('/html/body/div[12]/div/div[3]/span[1]/button')
        next_btn.click()

        type_choice = webdriver.find_element_by_xpath('//*[@id="js_original_article_type"]/div/a/label')
        type_choice.click()
        technology_text = webdriver.find_element_by_xpath(
            '//*[@id="js_original_article_type"]/div/div/div/div/dl[2]/dd/dl[8]/dt/a')
        technology_text.click()
        # confirm next
        confirm_btn_xpath = '/html/body/div[12]/div/div[3]/span[3]/button'
        wait_element_visible(webdriver, confirm_btn_xpath)
        confirm_btn = webdriver.find_element_by_xpath(confirm_btn_xpath)
        confirm_btn.click()
        # select pictures
        pic_select_btn_xpath = '//*[@id="js_imagedialog"]'
        pic_select_btn = webdriver.find_element_by_xpath(pic_select_btn_xpath)
        webdriver.execute_script('arguments[0].click()', pic_select_btn)

        first_pic_xpath = '/html/body/div[12]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/ul/li[1]/label/div[1]'
        wait_element_visible(webdriver, first_pic_xpath)
        first_pic = webdriver.find_element_by_xpath(first_pic_xpath)
        first_pic.click()
        next_btn = webdriver.find_element_by_xpath('/html/body/div[12]/div/div[3]/span[1]')
        next_btn.click()
        time.sleep(2)
        finish_btn_xpath = '/html/body/div[12]/div/div[3]/span[3]'
        wait_element_visible(webdriver, finish_btn_xpath)
        finish_btn = webdriver.find_element_by_xpath(finish_btn_xpath)
        finish_btn.click()
        # publish
        wait_element_gone(webdriver, finish_btn_xpath)
        publish_article_in_wechat(webdriver)


def publish_article_in_wechat(webdriver):
    publish_btn_xpath = '//*[@id="js_send"]'
    wait_element_visible(webdriver, publish_btn_xpath)
    publish_btn = webdriver.find_element_by_xpath(publish_btn_xpath)
    webdriver.execute_script('arguments[0].click()', publish_btn)
    # publish_btn.click()
    group_publish_btn_xpath = '//*[@id="send_btn_main"]/div/a/label'
    wait_element_visible(webdriver, group_publish_btn_xpath)
    group_publish_btn = webdriver.find_element_by_xpath('//*[@id="send_btn_main"]/div/a/label')
    group_publish_btn.click()


def transform_markdown_towechat(webdriver, content):
    webdriver.get('http://blog.didispace.com/tools/online-markdown/')
    content_input = webdriver.find_element_by_xpath('//*[@id="input"]')
    content_input.clear()
    content = content.replace('"', '\\"').replace('\n', (' \\' + 'n ')).replace('\\"\\n\\"', '\\"\\\\n\\"')
    # content = 'hello' + ' \\' + 'n' + '\\ ' + 'world'
    dd = "arguments[0].value=\"%s\"" % content
    print('content is ' + dd)
    webdriver.execute_script(dd, content_input)
    copy_btn = webdriver.find_element_by_xpath('//*[@id="output"]/div[2]/button')
    copy_btn.click()


def get_data_content(f, pattern):
    line = f.readline()
    if pattern in line:
        item_array = line.split(':')
        if len(item_array) > 1:
            return item_array[1]
    else:
        return ''


def publish_article_in_jj(webdriver):
    publish_btn = webdriver.find_element_by_xpath(
        '//*[@id="juejin-web-editor"]/div[2]/header/div[2]/div[5]/div[1]/span')
    publish_btn.click()
    android_tag = webdriver.find_element_by_xpath(
        '//*[@id="juejin-web-editor"]/div[2]/header/div[2]/div[5]/div[2]/div[2]/div[2]/div[1]')
    android_tag.click()
    publish_btn_xpath = '//*[@id="juejin-web-editor"]/div[2]/header/div[2]/div[5]/div[2]/button'
    wait_element_visible(webdriver, publish_btn_xpath)
    time.sleep(2)
    publish_btn = webdriver.find_element_by_xpath(publish_btn_xpath)
    publish_btn.click()


UN_JJ_PATTERN = 'un_jj'
PW_JJ_PATTERN = 'pw_jj'
UN_WC_PATTERN = 'un_wc'
PW_WC_PATTERN = 'pw_wc'
TITLE_PATTERN = 'title'
AUTHOR_PATTERN = 'author'

if len(sys.argv) <= 1:
    pass
else:
    file_path = sys.argv[1]
    with open(file_path, 'r', encoding='utf-8') as f:
        un_jj = get_data_content(f, UN_JJ_PATTERN)
        pw_jj = get_data_content(f, PW_JJ_PATTERN)
        un_wc = get_data_content(f, UN_WC_PATTERN)
        pw_wc = get_data_content(f, PW_WC_PATTERN)
        title = get_data_content(f, TITLE_PATTERN)
        author = get_data_content(f, AUTHOR_PATTERN)
        content = ''
        line = f.readline()
        while line != '':
            if '```' == line:
                line = line.lstrip()
            content += line
            line = f.readline()
        print(
            'un_jj is ' + un_jj + ' pw_jj is ' + pw_jj + ' un_wc is ' + un_wc + ' pw_wc is ' + pw_wc + ' title is ' + title + ' author is ' + author +
            ' content is ' + content)
webdriver = webdriver.Chrome()
webdriver.maximize_window()
loginJueJin(webdriver, un_jj, pw_jj)
write_btn_xpath = '//*[@id="juejin"]/div[2]/div/header/div/nav/ul/li[3]/div/button'
wait_element_visible(webdriver, write_btn_xpath)
write_btn = webdriver.find_element_by_xpath(write_btn_xpath)
write_btn.click()

write_btn_xpath = '//*[@id="juejin-web-editor"]/div[2]/header/div[2]/button'
wait_element_visible(webdriver, write_btn_xpath)

write_btn = webdriver.find_element_by_xpath(write_btn_xpath)
write_btn.click()
input_content(webdriver, '//*[@id="juejin-web-editor"]/div[2]/header/input', title,
              '//*[@id="juejin-web-editor"]/div[2]/div/div[1]/div[1]/textarea', content)
publish_article_in_jj(webdriver)

# trans makedown to wechat text
# transform_markdown_towechat(webdriver, content)

# loginWeChat(webdriver)
# wait_element_visible(webdriver, '//*[@id="menuBar"]/li[4]/ul/li[3]/a/span/span', 100)
# source_btn = webdriver.find_element_by_xpath('//*[@id="menuBar"]/li[4]/ul/li[3]/a/span/span')
# source_btn.click()
# create_btn_xpath = '//*[@id="js_main"]/div[3]/div[1]/div[2]/div[2]/div/a[1]'
# wait_element_visible(webdriver, create_btn_xpath)
# current_window_handle = webdriver.current_window_handle
# create_btn = webdriver.find_element_by_xpath(create_btn_xpath)
# create_btn.click()
# window_handles = webdriver.window_handles
# for handle in window_handles:
#     if handle != current_window_handle:
#         webdriver.switch_to.window(handle)
#         input_content(webdriver, '//*[@id="title"]', 'title', '//*[@id="ueditor_0"]', 'content', is_wechat=True,
#                       author_xpath='//*[@id="js_author_area"]', author=author)
