import pynetbox 
import telebot
import re
import config

netbox = pynetbox.api(url=config.URL_NB, token=config.TOKEN_NB)

bot = telebot.TeleBot(config.TOKEN_TELE)

regex_ip = re.compile(config.REGEX_IP)


def search_prefix(ipaddr,prefix):
    """Lấy các thông tin của prefix
    :Param prefix: Là địa chỉ prefix truyền vào để lấy thông tin của prefix đó
    :Response: Trả về result là tổng hợp thông tin của prefix như: 
        Site, Status, Tenant, vlan, Description
    """
    try:
        single_prefix = netbox.ipam.prefixes.get(prefix='{}' .format(ipaddr), mask_length='{}' .format(prefix))
        ip_prefix = ''
        status_prefix = ''
        descr_prefix = ''
        if single_prefix.prefix:
            ip_prefix = single_prefix.prefix
        if single_prefix.status:
            status_prefix = single_prefix.status
        try:
            site_prefix = single_prefix.site.name
        except:
            site_prefix ='null'
        try:
            tenant_prefix = single_prefix.tenant.name
        except:
            tenant_prefix = 'null'
        try: 
            vlan_prefix = single_prefix.vlan.name
        except:
            vlan_prefix ='null'
        if single_prefix.description:
            descr_prefix = single_prefix.description

        result = "Prefix" + " : " + '`'+ ip_prefix +'`'+ "\n" 
        result = result + "Site" + " : " + '`'+ site_prefix + '`' + "\n"
        result = result + "Status" + " : " + '`'+ str(status_prefix) +'`'+ "\n"
        result = result + "Tenant" + " : " + '`'+ tenant_prefix +'`'+ "\n"
        result = result + "vlan" + " : " + '`' +  vlan_prefix + '`' + "\n"
        result = result + "Description" + " : " + '`'+ descr_prefix +'`'+ "\n" 
    except Exception as ex: 
        result = str(ex)
    return result


def list_prefix():
    """Lấy tất cả các prefix
    :Param : Không cần truyền vào các thông số,
    chỉ cần gọi hàm sẽ trả về kết quả.
    :Response: Trả về prefix_all bao gồm tổng số prefix và 
    liệt kê tất cả các prefix đó
    """
    try:
        prefix = netbox.ipam.prefixes.all()
        prefix_count = netbox.ipam.prefixes.count()
        prefix_all = 'Tổng số Prefix : ' 
        prefix_all = prefix_all + str(prefix_count) + '\n\n' + str(prefix)
    except Exception as ex:
        prefix_all = str(ex)
    return prefix_all

def search_ip_address(ipaddr, prefix):
    """Lấy thông tin của địa chỉ IP
    :Param : Truyền vào địa chỉ IP kèm netmask
    :Response: Trả về info_ipaddr là tổng hợp thông tin của ip address bao gồm:
         Interface, Description, Tenant, Created, Last update
    """
    try:
        single_ipaddr = netbox.ipam.ip_addresses.get(address='{}' .format(ipaddr), mask_length='{}' .format(prefix))
        interface_ip = ''
        descr_ip = ''
        create_ip = ''
        last_update_ip = ''
        tenant_ip = ''
        try:
            site_ip = single_ipaddr.interface.device.site
        except:
            site_ip = single_ipaddr.interface.device.site
        try:
            parent_ip = single_ipaddr.interface.device
        except:
            parent_ip = 'null'
        if single_ipaddr.interface:
            interface_ip = single_ipaddr.interface
        if single_ipaddr.description:
            descr_ip = single_ipaddr.description
        if single_ipaddr.created:
            create_ip = single_ipaddr.created
        if single_ipaddr.last_updated:
            last_update_ip = single_ipaddr.last_updated
        if single_ipaddr.tenant:
            tenant_ip = single_ipaddr.tenant
        info_ipaddr = "Device" + " : " 
        info_ipaddr = info_ipaddr + '`' + str(parent_ip) + '`' + "\n" 
        info_ipaddr = info_ipaddr + "Interface" + " : " 
        info_ipaddr = info_ipaddr + '`' + str(interface_ip) + '`' + "\n"
        info_ipaddr = info_ipaddr + "Description" + " : " 
        info_ipaddr = info_ipaddr + '`' + str(descr_ip) + '`' + "\n"
        info_ipaddr = info_ipaddr + "Tenant" + " : " 
        info_ipaddr = info_ipaddr + '`' + str(tenant_ip) + '`' + "\n"
        info_ipaddr = info_ipaddr + "Site" + " : "
        info_ipaddr = info_ipaddr + '`' + str(site_ip) + '`' + "\n"
        info_ipaddr = info_ipaddr + "Created" + " : " 
        info_ipaddr = info_ipaddr + '`' + str(create_ip) + '`' + "\n"
        info_ipaddr = info_ipaddr + "Last updated" + " : " 
        info_ipaddr = info_ipaddr + '`' + str(last_update_ip) + '`' + "\n"
    except Exception as ex: 
        info_ipaddr = str(ex)
    return info_ipaddr

def list_ip_address():
    """Lấy tất cả các IP hiện có
    :Param : Không cần truyền vào các thông số,
    chỉ cần gọi hàm sẽ trả về kết quả.
    :Response: Trả về ipaddr_all bao gồm tổng số prefix và
    liệt kê tất cả các prefix đó
    """
    try:
        ipaddr = netbox.ipam.ip_addresses.all()
        ipaddr_count = netbox.ipam.ip_addresses.count()
        ipaddr_all = 'Tổng số IP addresses : ' 
        ipaddr_all = ipaddr_all + str(ipaddr_count) + '\n\n' + str(ipaddr)
    except Exception as ex:
        ipaddr_all = str(ex)
    return ipaddr_all

def search_device(device):
    """Lấy thông tin của device
    :Param : Truyền vào tên của thiết bị 
    :Response: Trả về info_device là tổng hợp các thông tin của device như :     
    Tenant, Role, Site, Type, Rack, Ipaddress, U, Platform, Serial, Assetag
    """

    try:
        single_device = netbox.dcim.devices.get(name='{}' .format(device))
        name_device = ''
        tenant_device = ''
        role_device = ''
        type_device = ''
        site_device = ''
        rack_device = ''
        ipddr_device = ''
        asetag_device = ''
        serial_device = ''
        u_device = ''
        platform_device = ''
        create_device = ''
        update_device = ''

        if single_device.name:
            name_device = single_device.name
        if single_device.tenant:
            tenant_device = single_device.tenant
        if single_device.device_role:
            role_device = single_device.device_role
        if single_device.device_type:
            type_device = single_device.device_type
        if single_device.site:
            site_device = single_device.site
        if single_device.rack:
            rack_device = single_device.rack
        if single_device.primary_ip:
            ipddr_device = single_device.primary_ip
        if single_device.asset_tag:
            asetag_device = single_device.asset_tag
        if single_device.serial:
            serial_device = single_device.serial
        if single_device.position:
            u_device = single_device.position
        if single_device.platform:
            platform_device = single_device.platform
        if single_device.created: 
            create_device = single_device.created
        if single_device.last_updated:
            update_device = single_device.last_updated

        info_device = "Name" + " : " 
        info_device = info_device + '`' + str(name_device) + '`' + "\n"
        info_device = info_device + "Tenant" + " : " 
        info_device = info_device + '`' + str(tenant_device) + '`' + "\n"
        info_device = info_device + "Role" + " : " 
        info_device = info_device + '`' + str(role_device) + '`' + "\n"
        info_device = info_device + "Type" + " : " 
        info_device = info_device + '`' + str(type_device) + '`' + "\n"
        info_device = info_device + "Site" + " : " 
        info_device = info_device + '`' + str(site_device) + '`' + "\n"
        info_device = info_device + "Rack" + " : " 
        info_device = info_device + '`' + str(rack_device) + '`' + "\n"
        info_device = info_device + "IPaddress" + " : " 
        info_device = info_device + '`' + str(ipddr_device) + '`' + "\n"
        info_device = info_device + "U" + " : " 
        info_device = info_device + '`' + str(u_device) + '`' + "\n"
        info_device = info_device + "Platform" + " : " 
        info_device = info_device + '`' + str(platform_device) + '`' + "\n"
        info_device = info_device + "Serial" + " : " 
        info_device = info_device + '`' + str(serial_device) + '`' + "\n"
        info_device = info_device + "Assetag" + " : " 
        info_device = info_device + '`' + str(asetag_device) + '`' + "\n"
        info_device = info_device + "Created" + " : " 
        info_device = info_device + '`' + str(create_device) + '`' + "\n"
        info_device = info_device + "Last Update" + " : " 
        info_device = info_device + '`' + str(update_device) + '`' + "\n"
    except Exception as ex:
        info_device = str(ex)
    return info_device

def device_comment(device):
    """Lấy thông tin comment của device
    :Param device: Truyền vào tên của thiết bị
    :Response: Trả về kết quả là comment của thiết bị 
    """
    try:
        single_device = netbox.dcim.devices.get(name='{}' .format(device))
        comment = "no comment"
        if single_device.comments:
            comment = single_device.comments
        device_comment = "Comments" + " : " + "\n" + str(comment)
    except Exception as ex: 
        device_comment = str(ex)
    return device_comment

def list_device():
    """Lấy tất cả các device 
    :Param : Không cần truyền vào các thông số,
    chỉ cần gọi hàm sẽ trả về kết quả.
    :Response: Trả về device_all bao gồm tổng số prefix và
    liệt kê tất cả các prefix đó
    """
    try:
        devices = netbox.dcim.devices.all()
        device_count = netbox.dcim.devices.count()
        device_all = 'Tổng số device : ' 
        device_all = device_all + str(device_count) + '\n\n' + str(devices)
    except Exception as ex:
        device_all = str(ex)
    return device_all

@bot.message_handler(commands=["start"])
def send_devices(message):
    """
        Tạo lệnh start để hướng dẫn sử dụng 
    """
    bot.reply_to(message,
        'Nhập vào /allprefix để xem' + 
        'tất cả các prefix' + '\n\n' + 
        'Nhập /prefix <ip/netmask> để xem' + 
        'thông tin của từng prefix. VD: /prefix 10.10.10.0/24' + '\n\n'+
        'Nhập vào /allipaddr để xem tất cả các IP address' + '\n\n' +
        'Nhập /ipaddr <ip/netmask> để xem' + 
        'thông tin của từng địa chỉ IP. VD: /ipaddr 10.10.10.10/24'+'\n\n'+
        'Nhập vào /alldevice để xem tất cả các device' + '\n\n' +
        'Nhập /device <tên thiết bị> để xem' + 
        'các thông tin của từng device. VD: /device SERVER-IDS')

def main():

    @bot.message_handler(commands=["prefix"])
    def send_prefix(message):
        """
            Tạo lệnh để truyền vào prefix từ telegram 
        """
        IP = message.text[8:]
        same_ip = regex_ip.match(IP)
        if same_ip :
            prefix = IP[-2:]
            result = search_prefix(IP,prefix)
            try:
                bot.send_message(config.CHAT_ID,
                                 str(result), parse_mode='Markdown')
            except:
                bot.send_message(config.CHAT_ID,
                                 str(result))
        else:
            bot.send_message(config.CHAT_ID,
                             'Nhập sai rồi !!',parse_mode='Markdown')
 
    @bot.message_handler(commands=["ipaddr"])
    def send_ip(message):
        """
            Tạo lệnh để truyền vào ip address từ telegram 
        """
        IP = message.text[8:]
        same_ip = regex_ip.match(IP)
        if same_ip :
            prefix = IP[-2:]
            result = search_ip_address(IP, prefix)
            try:
                bot.send_message(config.CHAT_ID,
                                 str(result), parse_mode='Markdown')
            except:
                bot.send_message(config.CHAT_ID,
                                 str(result))
        else:
            bot.send_message(config.CHAT_ID,
                             'Nhập sai rồi !!', parse_mode='Markdown')

    @bot.message_handler(commands=["device"])
    def send_device(message):
        """
            Tạo lệnh để truyền vào device từ telegram 
        """
        DEVICE = message.text[8:]
        info_device = search_device(DEVICE)
        comment = device_comment(DEVICE)
        try:
            bot.send_message(config.CHAT_ID,
                             str(info_device), parse_mode='Markdown')
        except:
            bot.send_message(config.CHAT_ID,str(info_device))
        try:
            bot.send_message(config.CHAT_ID,
                             str(comment), parse_mode='Markdown')
        except:
            bot.send_message(config.CHAT_ID,str(comment))

    @bot.message_handler(commands=["alldevice"])
    def send_device_all(message):
        """
            Tạo lệnh nhập /alldevice từ tele để lấy tất cả các device
            Nếu số ký tự gửi về telegram lớn hơn 4096,
        sẽ chia ra gửi thành nhiều message
        """
        device_all = list_device()
        if len(device_all) > 4096:
            for x in range(0, len(device_all), 4096):
                try:
                    bot.send_message(config.CHAT_ID,
                                     device_all[x:x+4096],
                                     parse_mode='Markdown')
                except:
                    bot.send_message(config.CHAT_ID,
                                     device_all[x:x+4096])
        else:
            try:
                bot.send_message(config.CHAT_ID,
                                 device_all, parse_mode='Markdown')
            except:
                bot.send_message(config.CHAT_ID,
                                 device_all)

    @bot.message_handler(commands=["allprefix"])
    def send_prefix_all(message):
        """
            Tạo lệnh nhập /allprefix từ tele để lấy tất cả các prefix
            Nếu số ký tự gửi về tele lớn hơn 4096,
        sẽ chia ra gửi thành nhiều message
        """
        prefix_list = list_prefix()
        prefix_all = str(prefix_list)
        if len(prefix_all) > 4096:
            for x in range(0, len(prefix_all), 4096):
                try:
                    bot.send_message(config.CHAT_ID,
                                     prefix_all[x:x+4096],
                                     parse_mode='Markdown')
                except:
                    bot.send_message(config.CHAT_ID,
                                     prefix_all[x:x+4096])
        else:
            try:
                bot.send_message(config.CHAT_ID,
                                 prefix_all, parse_mode='Markdown')
            except:
                bot.send_message(config.CHAT_ID,
                                 prefix_all)

    @bot.message_handler(commands=["allipaddr"])
    def send_ip_all(message):
        """
            Tạo lệnh nhập /allipaddr từ tele để lấy tất cả các ip address
            Nếu số ký tự gửi về tele lớn hơn 4096,
        sẽ chia ra gửi thành nhiều message
        """
        ipaddr_list = list_ip_address()
        ipaddr_all = str(ipaddr_list)
        if len(ipaddr_all) > 4096:
            for x in range(0, len(ipaddr_all), 4096):
                try:
                    bot.send_message(config.CHAT_ID,
                                     ipaddr_all[x:x+4096], parse_mode='Markdown')
                except:
                    bot.send_message(config.CHAT_ID,
                                     ipaddr_all[x:x+4096])
        else:
            try:
                bot.send_message(config.CHAT_ID,
                                 ipaddr_all, parse_mode='Markdown')
            except:
                bot.send_message(config.CHAT_ID,
                                 ipaddr_all)
    bot.polling()