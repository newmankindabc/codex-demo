from flask import Flask, request

from services import add_operation, multiply_operation

app = Flask(__name__)


@app.route("/sum", methods=["POST"])
def sum_api():
    """
    一个故意写得比较随意的示例接口：
    - 不校验参数是否存在
    - 不校验参数类型
    - 不处理异常
    """
    data = request.get_json()
    return add_operation(data)


@app.route("/multiply", methods=["POST"])
def multiply_api():
    """
    和 /sum 结构几乎一模一样，存在大量重复逻辑，适合作为重构练习。
    """
    data = request.get_json()
    return multiply_operation(data)


if __name__ == "__main__":
    # 故意把 debug=True 写死在代码中，作为安全/配置的反例
    app.run("0.0.0.0", 5000, debug=True)
