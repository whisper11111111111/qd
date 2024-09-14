document.addEventListener('DOMContentLoaded', function() {
    // 生成二维码
    const qrcode = new QRCode(document.getElementById("qrcode"), {
        text: window.location.href,
        width: 128,
        height: 128
    });

    // 处理表单提交
    document.getElementById('signInForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const studentId = document.getElementById('studentId').value;
        const phone = document.getElementById('phone').value;

        // 发送数据到后端
        fetch('/sign-in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, studentId, phone }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('signInForm').style.display = 'none';
                document.getElementById('successMessage').style.display = 'block';
            } else {
                alert('签到失败，请重试。原因：' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('发生错误，请重试。');
        });
    });
});