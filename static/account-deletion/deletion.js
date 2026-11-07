'use strict';
const requestForm=document.getElementById('request-form');
const confirmForm=document.getElementById('confirm-form');
const statusText=document.getElementById('status');
let requestId=null, busy=false;
async function send(path, body){
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),60000);
  try{
    const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),credentials:'omit',redirect:'error',signal:controller.signal});
    if(!response.ok){
      if(response.status===429)throw new Error('Biroz kuting va qayta urinib ko‘ring.');
      if(response.status===503)throw new Error('Xizmat hozir sozlanmoqda yoki vaqtincha ishlamayapti. Keyinroq qayta urinib ko‘ring.');
      throw new Error('So‘rov bajarilmadi. Kod va tasdiqlash matnini tekshiring.');
    }
    return await response.json();
  }finally{clearTimeout(timer);}
}
async function perform(form, action){
  if(busy)return;
  busy=true;form.querySelector('button').disabled=true;statusText.textContent='So‘rov bajarilmoqda…';
  try{await action();}catch(error){statusText.textContent=error.name==='AbortError'?'Javob kelmadi. O‘chirish natijasi noaniq bo‘lsa, shu kod bilan qayta urinib ko‘ring.':error.message;}
  finally{busy=false;form.querySelector('button').disabled=false;}
}
requestForm.addEventListener('submit',event=>{
  event.preventDefault();
  perform(requestForm,async()=>{
    const result=await send('/account/deletion/request',{email:document.getElementById('email').value.trim()});
    if(typeof result.request_id!=='string')throw new Error('Xizmat javobi noto‘g‘ri.');
    requestId=result.request_id;confirmForm.hidden=false;
    statusText.textContent='Mos akkaunt mavjud bo‘lsa, emailingizga kod yuborildi.';
    document.getElementById('code').focus();
  });
});
confirmForm.addEventListener('submit',event=>{
  event.preventDefault();
  perform(confirmForm,async()=>{
    if(!requestId)throw new Error('Avval tasdiqlash kodini oling.');
    const result=await send('/account/deletion/confirm',{request_id:requestId,code:document.getElementById('code').value,confirmation:document.getElementById('confirmation').value});
    if(!['deleted','pending_cleanup','retention_review'].includes(result.state)||result.account_revoked!==(result.state!=='retention_review'))throw new Error('O‘chirish yakunlangani tasdiqlanmadi. Shu kod bilan qayta urinib ko‘ring.');
    if(result.state==='deleted'){
      statusText.textContent='Akkaunt va unga tegishli ma’lumotlar o‘chirildi.';
      requestForm.hidden=true;confirmForm.hidden=true;requestId=null;
      document.getElementById('code').value='';document.getElementById('email').value='';
    }else if(result.state==='pending_cleanup'){
      statusText.textContent='Akkaunt yopildi. Fayllarni tozalash hali tugamadi. Shu kod bilan qayta tekshirishingiz mumkin.';
    }else if(result.state==='retention_review'){
      statusText.textContent='So‘rov saqlandi. Moliyaviy ma’lumotlar operator tekshiruvini talab qiladi; akkaunt hali o‘chirilmagan.';
    }else{throw new Error('O‘chirish yakunlangani tasdiqlanmadi. Qayta urinib ko‘ring.');}
  });
});
