<form method="post" action="https://ums.dreamline.co.kr/API/send_kkt.php">
    <input type='text' name='id_type' value='MID'/> # 로그인 방식
    <input type='text' name='id' value='dreamcloud'/> # 웹 접속 ID
    <input type='text' name='auth_key' value='365e0742183b71e950ca7c3dce3b41a0'/> # 인증키
    <input type='text' name='msg_type' value='KAT'/> # 전송할 메시지 타입
    <input type='text' name='callback_key' value='aa95b42929a5dff649874c8df5b87a4d946c0669'/> # 발신프로필키
    <input type='text' name='send_id_receive_number' value='send_id1|01030056900'/> 
    <input type='text' name='template_code' value='dream'/> # ums.dreamline.co.kr -> 마이페이지 -> 카카오톡관리 -> 템플릿
    <input type='text' name='content' value='test_kakao'/>
    <input type='text' name='resend' value='NONE'/> # 실패시 재전송 (SMS, LMS, NONE)
    <input type="submit" name="submit" value='OK' />
</form>