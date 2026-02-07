from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Cyber Traffic Rule</title>
<style>
body{
    background:linear-gradient(135deg,#0b132b,#1c2541);
    color:white;
    font-family:Arial;
    text-align:center;
    padding-top:30px;
}
.header{
    font-size:32px;
    margin-bottom:10px;
}
.sub{
    font-size:16px;
    opacity:0.9;
}
input{
    width:65%;
    padding:12px;
    font-size:16px;
    margin-top:20px;
}
button{
    padding:12px 25px;
    font-size:16px;
    margin-top:15px;
    cursor:pointer;
}
.light{
    width:100px;
    height:100px;
    border-radius:50%;
    margin:25px auto;
    background:gray;
}
.green{background:lime;}
.yellow{background:yellow;}
.red{background:red;}
.box{
    font-size:18px;
    margin-top:10px;
}
.footer{
    margin-top:30px;
    font-size:14px;
    opacity:0.7;
}
</style>
</head>

<body>

<div class="header">🚦 Cyber Traffic Rule</div>
<div class="sub">Link Safety Detection System</div>

<form method="POST">
<input name="link" placeholder="Paste any website link here" required>
<br>
<button type="submit">Check Link</button>
</form>

{% if status %}
<div class="light {{ status }}"></div>

<div class="box">
<b>Status:</b> {{ status|upper }} <br>
<b>Risk:</b> {{ risk }}% <br>
<b>Reason:</b> {{ reason }}
</div>
{% endif %}

{% if status == "red" %}
<audio autoplay>
  <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
</audio>
{% endif %}

<div class="footer">
Cyber Safety Awareness Project
</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    status=""
    risk=0
    reason=""

    if request.method=="POST":
        link=request.form["link"].lower().strip()

        status="green"
        risk=10
        reason="Safe link"

        # 🔴 Dangerous
        if (
            link.startswith("http://") or
            "@" in link or
            re.search(r"\d+\.\d+\.\d+\.\d+", link) or
            any(w in link for w in ["login","otp","bank","verify","password"])
        ):
            status="red"
            risk=90
            reason="Dangerous / phishing link"

        # 🟡 Suspicious
        elif (
            any(s in link for s in ["bit.ly","tinyurl","t.co"]) or
            len(link) > 70
        ):
            status="yellow"
            risk=55
            reason="Suspicious link"

    return render_template_string(HTML,status=status,risk=risk,reason=reason)

if __name__=="__main__":
    app.run(debug=True)