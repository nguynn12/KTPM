# TV3 — Tập nói và trả lời nhanh

## Mở đầu khoảng 30 giây
Em là Nguyễn Khiêm Thuận, phụ trách nghiên cứu Schemathesis và kế hoạch kiểm thử, tương ứng Phần D và E. Em xác định phạm vi API, điều kiện chạy, cách đánh giá pass/fail và thiết kế ca kiểm thử bổ sung. Seed cá nhân của em là 303; kết quả thực thi chỉ được báo cáo từ log của lượt chạy trên máy em.

## Câu hỏi dễ được hỏi
1. **Schemathesis là gì?** Công cụ sinh kiểm thử API từ OpenAPI/GraphQL. Đề tài này dùng OpenAPI của Paperless, sinh input và kiểm tra phản hồi theo các thuộc tính/hợp đồng.
2. **Schema có gì?** Path, method, parameter, body, kiểu/ràng buộc dữ liệu và mô tả response. Không phải schema cơ sở dữ liệu.
3. **Vì sao dùng công cụ này?** Tự thử nhiều input và trường hợp biên; phát hiện lỗi server hoặc lệch hợp đồng. Vẫn phải bổ sung test nghiệp vụ.
4. **Seed 303 là số test à?** Không. Là đầu vào điều khiển sinh ngẫu nhiên của TV3. 25 max-examples cũng không phải tổng số request thực tế.
5. **Cùng seed chắc chắn cùng lỗi không?** Không bảo đảm chỉ nhờ seed. Cần phiên bản, schema, baseline, flags/phases và trạng thái môi trường phù hợp; tái hiện bằng request tối thiểu đáng tin hơn.
6. **Ba vòng khác nhau ở đâu?** Vòng 1 GET bốn nhóm; vòng 2 đọc/ghi ba nhóm danh mục; vòng 3 thêm documents và chạy all checks. Mỗi vòng ghi cần reset/seed và lưu log riêng.
7. **HTTP 400 có phải Fail?** Không mặc định. Input sai bị từ chối đúng là đạt kiểm tra validation; nếu schema không mô tả 400 thì còn lỗi hợp đồng riêng.
8. **HTTP 201 là Pass chắc chắn?** Chưa. Body phải đúng schema và nghiệp vụ; thiếu trường required vẫn là failure.
9. **404 nghĩa là phần mềm lỗi?** Chưa. Với ID không tồn tại, 404 là đúng. Muốn test GET thành công phải dùng ID thật từ fixture.
10. **Vì sao reset?** Fuzzing có thể tạo/sửa/xóa dữ liệu. Baseline khác nhau làm sai việc so sánh và khó tái hiện.
11. **Reset API đủ chưa?** Chưa chắc. Phải xử lý hết phân trang, trash/tác vụ; reset volume xóa toàn bộ dữ liệu nên cần xác nhận và seed lại.
12. **Em thiết kế biên thế nào?** Xác minh L trong schema, thử rỗng, L-1, L, L+1 và quá dài; phân biệt hợp lệ/không hợp lệ rồi xác định expected trước khi chạy.
13. **Một failure có phải một bug?** Không. Một bug có thể tạo nhiều failure ở nhiều input/checks. Phải gom theo nguyên nhân và tái hiện.
14. **Ba bug của TV2 có phải em tìm được?** Không. Em ghi rõ người phát hiện; chỉ nhận đã tái hiện khi có request/response và log riêng.
15. **Phần việc của em là gì?** Chuẩn hóa cách chạy, nguyên lý K05, kế hoạch phạm vi/giả định/rủi ro/oracle và test scenario. Số liệu chạy cá nhân bổ sung bằng log seed 303.
16. **All checks có kiểm tra hết hệ thống không?** Không. Phụ thuộc bộ checks bản cài và endpoints/phases được chọn, không thay UI, load test, OCR accuracy hay security audit.
17. **Upload xong là OCR thành công chưa?** Chưa. Phải chờ task, thấy tài liệu và nội dung. File TXT chỉ là nhập văn bản; OCR ảnh cần bằng chứng nhận dạng ảnh/scan.
18. **Vì sao số test em khác TV2?** Seed khác; ngoài ra TV2 vòng 1 còn có phạm vi rộng hơn. Chưa thể so số lượng nếu cấu hình, dữ liệu, schema/phases không đồng nhất.

## Trước khi báo cáo
Mở Notes của slide để tập nói. Dùng lời hiện tại đúng trạng thái: đã soạn kế hoạch; đã chạy chỉ khi có log. Nếu bị chặn, nói chính xác vòng nào chưa chạy và lý do, không che thành pass. Kịch bản demo ưu tiên vòng GET ngắn có nhãn smoke; không chạy reset hoặc vòng ghi trước lớp khi chưa chuẩn bị.
