# Check serial number:

## Tổng quan:

+ Mục đích của chương trình này là kiểm tra tính chính xác của serial number giữa file "inputs.yml" và serial number đọc được từ Inverter. Giúp cho số liệu thu về được đúng với thiết bị.

+ Để xác định được Inverter nào thì sẽ thông qua địa chỉ IP/port và ModbusUnitID (các thông số này sẽ lấy ở file "inputs.yml").

## Các bước tiến hành kiểm tra serial number:

1. Chạy file "checkSN.py";

2. Nhập vào đường dẫn file "inputs.yml" tại site cần check;

3. Vào file "runtime.log" để xem thông tin và chỉnh sửa lại nếu số serial của file input khác với số serial đọc ở inverter.

### Sẽ có 3 trường hợp:

+ Không kết nối vào được IP/port của Inverter. Cần kiểm tra lại xem đúng IP đích chưa.

+ Đúng serial number và kết thúc kiểm tra.

+ Sai serial number và cần phải sửa lại serial number bị sai ở file "inputs.yml".