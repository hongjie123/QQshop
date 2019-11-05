
#老师的代码
from alipay import AliPay
def Pay(order_id,money):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjZrMpDxpfV2UwLV833KoMxsjSLQu93WtDiNI7mITLavWo/OZharkGGC44e5OWQo2+df8mkhA9g+7lSHYuQQU3uNJhpB8z1bkgUgZ8jlZWtUzGAb9aJfJS4ZoZAVmcPQJMLPDabJctJyGSRO0u0dSGX/ojQjcyDRIiZ1xAC+SLSzSPFhJsY9Wo4NV0/p4ut9GejWY101cYtLhee02M1oW2nO/naL6RNZrBAOo3y5ctxq/W2OQoOT/ZDs1EEoXzUSZCCTR90CWtxt8yw4lOwoDonKQKyrTB3gMFCsWj84A2Qp/FZ6EHH2XeGz2M9FhHRa/uWQQa8knDUxMI/8yZzuPEQIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEogIBAAKCAQEAjZrMpDxpfV2UwLV833KoMxsjSLQu93WtDiNI7mITLavWo/OZharkGGC44e5OWQo2+df8mkhA9g+7lSHYuQQU3uNJhpB8z1bkgUgZ8jlZWtUzGAb9aJfJS4ZoZAVmcPQJMLPDabJctJyGSRO0u0dSGX/ojQjcyDRIiZ1xAC+SLSzSPFhJsY9Wo4NV0/p4ut9GejWY101cYtLhee02M1oW2nO/naL6RNZrBAOo3y5ctxq/W2OQoOT/ZDs1EEoXzUSZCCTR90CWtxt8yw4lOwoDonKQKyrTB3gMFCsWj84A2Qp/FZ6EHH2XeGz2M9FhHRa/uWQQa8knDUxMI/8yZzuPEQIDAQABAoIBAB+undC1L4j8EhcXxAuedKGSlc9jeQqmyoRaQqwLR201gD2IeDXe6U/G/DaYgfEMBwbZW0wNlHM5S+fu/bVPg3fm9IFl/HbLYy7FugBm8mYPQ3JBxhrLsx7xwJN4XdYx04iQ/8y7OmCykJzzCsHIEEdiRd6gN/2XLQ+VKT44ZoUyp9QHoPqNk1iSKo+Pa7gubdVSGnOibLQE3i9Y8FR35s3fTzrJq26F4ZGA5Q9TPEnR+HtcMV4R+L7wLc61WIIMR2m0hb5B+Hr3OJcEgYN+Ft6WYeq0QmbEHBT4CqZ6dbsq42JI6IPkJZY2f0L17bQCVbsl+YAOz5BTW+Oi00nMxz0CgYEAwjHXVztc09bWYUr33pOk3mAyBj7eFx7dBfUarvmnTkx007lVeSBwxASpSYCUqVX5sgIacV9xYccamCYRrRCy8lC/4crF9v4MmjMi/WARywIbvP9W22x4HuimrePSGeYP34SMuLNTO9Bu4C4nFldi6e1kacCVjEioXqj/vM7dDYcCgYEAuqwl1DPGILZ59JekHBJqHyCzqsxOpsQHaue1HZeEvVCpIGgRILIfgDbqqRy0jystMsHntMTpSrznZ4/9dFUGHJB2SNV8eqiicCnflq898h2M0QWx1UxbGXq1bDT29SZVEXuo56mumdatGnLeC9EIW7c6SMG32E7zgGosJ84JZKcCgYB7yamrQXv6zYf6nP9EMnl2B3vb31dTBal+kq9fumSb1MDj9dA2VieLzCzdXcll6BgzEIQqoNx1p6WcNygtWee37yFhnRB0UZ1W7iHvwb2V2tIzt9B2Lr6jdUpKrl7Pg4e6w5OwaR81kbgbz0+7PhkfZOQNRWYO9oHdVX0vre3bIQKBgCM0pE3JFezFfWqrzr+cmXcVa80iixLYla2L1ZSnJtmthLgf6FsKPPapZMhQKZ12vyd7en+VQ4pc5ieZ+GsgPe7VL/m8iaV4eGo++3QnyL8I463oLQnVRLkhc2Xc91Z0zEZn1Asc7VkGK895KneADNt/Sva90jZxbWsimwFG0m6xAoGASAVJ99XRUFWagSDHoblkEHCs24Jxb4YO+JI20qHIo6OlfW21CtrqIkWcHale/DukEjjArIb7Dz7CYmIlFLjfWjvlqXh+HGdwvkagMZwxKXmsd6FkL4sBMi3QDln87GbviftlX1/0O/trIAtKIOjFlcNldjRFXwH8uqW7c+gJzKQ=
    -----END RSA PRIVATE KEY-----'''

    alipay = AliPay(
        appid="2016101500695747",  # 支付宝app的id
        app_notify_url="",  # 回调视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url="http://127.0.0.1:8000/Buyer/pay_result/", #完成之后返回
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/?out_order_id=%s"%order_id  # 可选, 支付状态被修改，调用的路由
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string

if __name__ == '__main__':
    print(Pay("100000003","1000"))