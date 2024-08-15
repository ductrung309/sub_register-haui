import requests
import json

print("Nhớ đọc hướng dẫn để lấy cookies và kverify của mình nhaaaaaa !!!")
cookies = input("Nhập vào cookies: ")
kverify = input("Nhập vào kverify: ")
ctdk = input("Nhập vào mã ngành: ")
properties = ['IndependentClassID','ModulesName', 'ClassCode', 'CountS', 'MaxStudent', 'ListDate']

# URL và dữ liệu yêu cầu
url = f'https://sv.haui.edu.vn/ajax/register/action.htm?cmd=classbymodulesid&v={kverify if kverify else "DAC31F70B5AA0E1D5B8CDEFD337C1D72"}'

# Thiết lập các tiêu đề yêu cầu giống như trong trình duyệt
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': cookies if cookies else '_ga_CFED63V11Q=GS1.1.1689637006.119.1.1689637070.0.0.0; UqZBpD3n=v1UR+GSQ__YGy; _ga_G1VDE91S1Z=GS1.3.1692008540.2.0.1692008540.0.0.0; __Host-UqZBpD3n=v1UR+GSQ__YGy; _ga_N1ND2KBTYH=GS1.1.1708497992.246.1.1708498029.0.0.0; _ga_M6W50XGDVZ=GS1.1.1708497989.134.1.1708498451.0.0.0; _ga_ZG0RX9N53W=GS1.3.1708656847.196.1.1708656890.0.0.0; _ga_61721GVZDB=GS1.1.1714381108.2.1.1714381145.23.0.0; _ga=GA1.1.707666577.1667897285; ASP.NET_SessionId=2abqsf2floiy4kso1pfrmywt; kVisit=ca9c32af-97cf-43db-81f5-8872cc0c4a88; onehauisv=A8E61DA724670420F16FDC718E3894EAC58501BEE87C92B95826A909A3427F445E07767C9120BAF0330EED6E0FAB8439ACFBBCF79CB2E78A172A01FF3A71CE17D771473545438FAE061777667D9ED44B60EC29D170B36D61E3818F8FB4C5F0EF05FBC36B6EADAD803D332AF30B228B81972E10A4392461D316F77435B566B65842195634C097E56086C03E60BA0C40C227F1BDF0D6174D74DBDBBBA155F2221CEEAC1BBF261328057476ECC8D46157BFA7A324755CA7E894CBF359B539E1F19B8533FD1AF23EF46E1886595D90A6FFBEB3D0E7F069C4CB5C25F874EB12009405141E22766C511CF206F060BC2760447889EBED0E11CCB9CC04C1956F277739B8A3410487CF2BBEB7F7930EC8B48111CD5B85A7A340D2E056DE670D9193A2562B958CD6A45F663809A8E3C30F4883AFADE4F7405F27B1524B0FF1080239A83B5E0A6FA0BFD4CDD53F27CCB7FAF8B69E9F786801D3AF67580EC80689B2AC4C2CA98D684889CA5307ACB602484FCDBAC97E743D877D47474C7E87DADB4C6E24F629; _ga_S8WJEW3D2H=GS1.1.1723707702.7.1.1723713881.0.0.0',
    'Referer': 'https://sv.haui.edu.vn/register/',
}

def addClass():
    class_id = input("Nhập vào id lớp học hiện trên màn hình: ")    
    # URL yêu cầu POST
    url = f'https://sv.haui.edu.vn/ajax/register/action.htm?cmd=addclass&v={kverify if kverify else "DAC31F70B5AA0E1D5B8CDEFD337C1D72"}'
    # Dữ liệu gửi kèm yêu cầu
    payload = {
        'class': class_id,
        'ctdk': ctdk if ctdk else 842
    }

    # Gửi yêu cầu POST
    response = requests.post(url, data=payload, headers=headers)

    # Xử lý phản hồi
    if response.status_code == 200:
        item = response.json()
        if item.get('err') == 0:
            print('Đăng ký thành công:', item.get('Message'))
            # Gọi hàm GetTableOrder nếu cần
        else:
            print('Đăng ký thất bại:', item.get('Message'))
    else:
        print(f'Yêu cầu thất bại với mã lỗi: {response.status_code}')

def classList(idSubj):
    try:
        # Gửi yêu cầu POST
        data = {'fid': int(idSubj) if idSubj else 6819}
        response = requests.post(url, data=data, headers=headers)
        # Kiểm tra mã trạng thái của phản hồi
        response.raise_for_status()
    
        # Phân tích cú pháp phản hồi JSON
        try:
            json_data = response.json()
            # Kiểm tra nếu json_data['data'] không phải là mảng rỗng
            if json_data.get('data') and len(json_data['data']) > 0:
                for Class in json_data['data']:
                    # Chuyển đổi các thuộc tính chuỗi JSON thành đối tượng Python
                    Class['GiaoVien'] = json.loads(Class['GiaoVien'])
                    Class['ListDate'] = json.loads(Class['ListDate'])
                
                    for key in properties:
                        if key in Class:
                            value = Class[key]
                            # Xử lý giá trị ListDate để in ra thông tin cụ thể nếu cần
                            if key == 'ListDate':
                                print(f"Thứ: {value[0]['DayStudy']} {value[1]['DayStudy'] if value[1]['DayStudy'] != value[0]['DayStudy'] and value[1]['DayStudy'] else ''}", end='Tiết: ')
                                for val in value:
                                    print(val["StudyTime"], end=" ")
                            elif key == 'CountS':
                                print(f"Số lượng: {value}", end="/")
                            elif key == "MaxStudent":
                                print(f"{value}", end= " || ")
                            else:
                                print(f"{key} : {value}", end=" || ")
                    print('')
            else:
                print('Không có dữ liệu để hiển thị')
        except ValueError:
            print('Lỗi giải mã JSON')
    except requests.RequestException as e:
        print(f'Lỗi yêu cầu HTTP: {e}')
    print("\n\n")    

while True:
    idSubj = input("Nhập vào mã học phần của môn: ")
    while True:
        print("1.Xem danh sách lớp\n2.Đăng kí học phần\n3.Đổi môn khác")
        check = input("Lựa chọn số: ")
        if check == '1':
            classList(idSubj= idSubj)
        elif check == '2':
            addClass()
        else:
            break