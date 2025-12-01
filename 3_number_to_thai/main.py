"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        if number == 0:
            return "ศูนย์"
        if number > 10000000:
            return "number out of range"

        th_num = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        th_unit = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

        def read_under_million(n):
            result = ""
            digits = list(map(int, str(n)))
            length = len(digits)

            for i, d in enumerate(digits):
                pos = length - i - 1  # ตำแหน่งหลัก เช่น หลักร้อย หลักสิบ ฯลฯ

                if d == 0:
                    continue

                # หลักสิบ
                if pos == 1:
                    if d == 1:
                        result += "สิบ"
                    elif d == 2:
                        result += "ยี่สิบ"
                    else:
                        result += th_num[d] + "สิบ"
                    continue

                # หลักหน่วย
                if pos == 0:
                    if d == 1 and length > 1:
                        result += "เอ็ด"
                    else:
                        result += th_num[d]
                    continue

                # หลักอื่นๆ (ร้อย พัน หมื่น แสน)
                result += th_num[d] + th_unit[pos]

            return result

        # ถ้ามีหลักล้าน
        if number >= 1000000:
            million_part = number // 1000000
            rest_part = number % 1000000

            if rest_part == 0:
                return read_under_million(million_part) + "ล้าน"
            else:
                return read_under_million(million_part) + "ล้าน" + read_under_million(rest_part)

        # น้อยกว่าล้าน
        return read_under_million(number)

s = Solution()
print(s.number_to_thai(55571))