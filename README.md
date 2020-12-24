# Netbox_Telegram

## 1. Giới thiệu : 

Netbox Telegram là 1 tool được viết bằng ngôn ngữ python, với mục đích để check các thông tin lưu trên netbox. Với mục đích là sự tiện lợi, có thể thao tác ngay trên telegram để check các thông tin mà không cần truy cập vào netbox trên web. 

Vì thông tin dữ liệu trên netbox là thông tin nhạy cảm nên theo mặc định chỉ có thể gửi về 1 ID duy nhất trên telegram.

## 2. Các tính năng

Tool có các chức năng khi thao tác trên telegram như : 

- [x] List all prefix

- [x] Check info single prefix

- [x] List all ip address

- [x] Check info single ip address

- [x] List all device 

- [x] Check info single device 

## 3. Cài đặt 

Cài đặt trên hệ điều hành CentOS 7 

Thực hiện bằng user với quyền sudo hoặc người dùng root

### Bước 1: Cài đặt các gói cần thiết

Ta kiểm tra xem đã có version 3 của python được cài trong máy chưa. 

```
python3 --version
```

Thực hiện cài đặt python3 và các gói cần thiết.

```
yum groupinstall "Development Tools" -y
yum install python3-devel -y
yum install python3 -y
yum install python3-pip -y
pip3 install virtualenv
yum install -y git wget
```

### Bước 2: Tải về source code

```
cd /opt
git clone https://github.com/nhanhoadocs/netbox-telegram.git
cd netbox-telegram
```

#### Chỉnh sửa file config.py

- Thêm token bot telegram 

```
sed -i 's/TOKEN_TELE =/TOKEN_TELE = "918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw"/' /opt/netbox-telegram/config.py
```

Thay `918364925:AAGbl5y7463f8DFFx4RhkeB3_eRhUUNfHHw` bằng token bot của bạn 

- Thêm message id telegram 

```
sed -i 's/CHAT_ID =/CHAT_ID = "633940211"/' /opt/netbox-telegram/config.py
```

Thay id `633940211` bằng chat của bạn hoặc của group muốn nhận tin nhắn

- Thêm vào url là đường dẫn đến trang netbox của bạn 

```
sed -i 's/URL_NB =/URL_NB = "https:\/\/netbox.hungnv.com"/' /opt/netbox-telegram/config.py
```

Thay `https://netbox.hungnv.com` bằng url đẫn đến trang netbox của bạn. Với mỗi dấu `/` trên url, ta phải thêm 1 dấu `\` vào trước nó. 

- Thêm vào token user của netbox. 

```
sed -i 's/TOKEN_NB =/TOKEN_NB = "933f6df395h3b23bdd103k582nf93l450d64b4d260"/' /opt/netbox-telegram/config.py
``` 

Thay token `933f6df395h3b23bdd103k582nf93l450d64b4d260` bằng token user trên netbox của bạn. 

Nếu chưa biết cách để lấy token, bạn có thể làm theo các bước sau : 

- Sau khi đăng nhập vào netbox, kích vào khu vực quản trị user : 

![](../images/netbox1.png)

- Kích vào tab user có hình bánh răng 

![](../images/netbox2.png)

- Ở mục token, kích vào Add token 

![](../images/netbox4.png)

- Lần lượt kích chọn user, ngày giờ hết hạn và lưu lại. 

![Imgur](../images/netbox5.png)

- Sau khi lưu ta sẽ có đoạn mã token. Hãy copy mã và điền vào file config. 

![Imgur](../images/netbox3.png)

**Kiểm tra lại file config**
Sau khi ghi vào file, kiểm tra lại file config để chắc chắn đã điền đủ các thông tin 

Sử dụng lệnh sau để kiểm tra : 

```
egrep -v "^*#|^$" /opt/netbox-telegram/config.py
```

Kết quả các trường đã điền thông tin như sau là ok 

![Imgur](../images/netbox6.png)

### Bước 3: Tạo venv 

#### Tạo môi trường ảo python 

```
cd /opt/netbox-telegram
virtualenv env -p python3.6
source env/bin/activate
```
#### Cài đặt requirement 

```
pip install -r requirements.txt
```

### Bước 4: Tạo file service để chương trình chạy như 1 dịch vụ 

#### Tạo file service

```
vi /etc/systemd/system/netboxinfo.service
```

và ghi vào file nội dung như sau : 

```
[Unit]
Description= Get data on netbox
After=network.target

[Service]
PermissionsStartOnly=True
User=root
Group=root
ExecStart=/opt/netbox-telegram/env/bin/python3 /opt/netbox-telegram/main.py --serve-in-foreground

[Install]
WantedBy=multi-user.target
```

#### Khởi động dich vụ netboxinfo

```
systemctl daemon-reload
systemctl start netboxinfo
systemctl status netboxinfo
systemctl enable netboxinfo
```
### Bước 5 : Đặt crontab check service 

Để phòng các trường hợp dẫn đến service bị tắt, mình sẽ đặt 1 cron để check nếu service vì bất kỳ lý do gì bị tắt, sẽ tự động khởi động lại service đó. 

```
cd /opt/netbox-telegram
chmod +x checkservice.sh
```
- Ghi vào dịch vụ muốn giám sát.

```
sed -i 's/SERVICES=/SERVICES="netboxinfo"/' /opt/netbox-telegram/checkservice.sh
```

- Sử dụng lệnh `crontab -e` và lưu đoạn cấu hình sau vào file crontab : 

cron check 20 phút 1 lần. Nếu dịch vụ tắt sẽ tự khởi động lại. 

```
*/20 * * * * /opt/netbox-telegram/checkservice.sh > /dev/null 2>&1
```

## 4. Demo 

Sau khi khởi động, truy cập trực tiếp vào bot hoặc nhóm có  bot là thành viên để sử dụng bot. (tùy vào message id bạn đặt ở đâu)

Nhập vào `/start` để bắt đầu sử dụng bot.

![Imgur](https://i.imgur.com/GwGToRh.png)

Sau khi nhập vào start, sẽ có những hướng dẫn để bạn có thể sử dụng thao tác với bot để lấy thông tin. 

- Muốn xem tất cả các device hiện có, ta sử dụng `/alldevice` 

![Imgur](../images/netbox8.png)

- Muốn xem tất cả các prefix hiện có, ta sử dụng `/allprefix` 

![Imgur](../images/netbox7.png)

- Muốn xem tất cả các IP address hiện có, ta sử dụng `/allipaddr` 

![Imgur](../images/netbox9.png)

- Để xem thông tin của từng IP, ta sử dụng `ipaddr` kèm địa chỉ IP

![Imgur](../images/netbox10.png)

- Để xem thông tin của từng thiết bị, ta sử dụng `device` kèm tên thiết bị 

![Imgur](../images/netbox11.png)

- Để xem thông tin của từng prefix, ta sử dụng `prefix` kèm địa chỉ prefix 

![Imgur](../images/netbox12.png)

