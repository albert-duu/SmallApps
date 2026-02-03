import streamlit as st
import urllib.request
import json

# 设置页面标题
st.set_page_config(page_title="酒店积分价值计算器", page_icon="🏨")
st.title("🏨 Marriott Points value check")
st.write("输入积分与现金价格，快速判断是否值得兑换")

@st.cache_data(ttl=86400)  # cache for 1 day
def get_exchange_rate(currency_code):
    url = f"https://open.er-api.com/v6/latest/{currency_code}"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data['rates']['USD']

col1, col2, col3, col4 = st.columns(4)

with col1:
    points = st.number_input("所需积分", min_value=1, value=40000, step=1000)
with col2:
    local_price = st.number_input("现金价格 (含税)", min_value=0.0, value=40000.0, step=1000.0)
with col3:
    currency = st.selectbox("货币种类", [
        "JPY", "USD", "EUR", "GBP", "CNY", "CAD", "AUD", "CHF", "HKD", "SGD", 
        "NZD", "KRW", "INR", "TWD", "THB", "MXN", "ZAR", "BRL", "SEK", "NOK"
    ])
with col4:
    target_cpp = st.number_input("目标基准线 (cpp)", min_value=0.1, max_value=5.0, value=0.8, step=0.1)

# click button to start calculation
if st.button("开始计算 ✨", type="primary"):
    with st.spinner('正在获取实时汇率...'):
        try:
            exchange_rate = get_exchange_rate(currency)
            
            # 计算逻辑
            price_usd = local_price * exchange_rate
            cpp = (price_usd / points) * 100
            
            st.markdown("---")
            
            # 展示主要结果
            if cpp > target_cpp:
                st.success(f"✅ 划算！当前积分价值为 **{cpp:.2f} 美分/分**，高于你设定的 {target_cpp} 美分标准。")
                st.balloons() # 增加庆祝特效
            else:
                st.error(f"❌ 不划算！当前积分价值仅为 **{cpp:.2f} 美分/分**，低于你设定的 {target_cpp} 美分标准，建议使用现金预订。")

            # 展示数据明细
            col_res1, col_res2, col_res3 = st.columns(3)
            col_res1.metric("折合美元", f"${price_usd:.2f}")
            col_res2.metric("当前汇率", f"1 {currency} = ${exchange_rate:.4f}")
            col_res3.metric("每分价值 (CPP)", f"{cpp:.2f} ¢")

        except Exception:
            st.error("获取汇率失败，请检查网络连接。")