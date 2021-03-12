# import subprocess so we can use system commands
import subprocess
# regular expressions.
import re

# 等於在CMD輸入netsh wlan show profiles
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout

# 用正規表示法搜尋全部本機wifi名稱
profile_names = (re.findall("ALL User Profile     : (.*)\r", command_output))

# 儲存username or password
wifi_list = list()

# 如果儲存在本機的wifi不為0
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        # 介面 Wi-Fi 上的設定檔
        profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", name], capture_output=True).stdout.decode()
        # 如果沒有密碼continue掉
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile['ssid'] = name
            # 有密碼必須設key為clear才能取得密碼
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profiles", name, "key=clear"],capture_output=True).stdout.decode()
            # 找到密碼
            password = re.search("Key Content             (.*)\r", profile_info_pass)
            # 如果沒有密碼，設置密碼為None
            if password == None:
                wifi_profile["password"] = None
            else:
                # 否的話將指定密碼
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)
# 遍歷資料列印出來
for x in range(len(wifi_list)):
    print(wifi_list[x])
