'use strict';
const el=id=>document.getElementById(id);
let proof=null, busy=false, available=false;
const status=message=>{el('status').textContent=message;};
async function api(path,body){
  const controller=new AbortController(), timer=setTimeout(()=>controller.abort(),60000);
  try{
    const response=await fetch(path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json'},
      ...(body?{body:JSON.stringify(body)}:{}),credentials:'omit',redirect:'error',signal:controller.signal});
    if(!response.ok)throw new Error(response.status===429?'Biroz kutib qayta urinib ko‘ring.':
      response.status===503?'Xizmat hali tayyor emas yoki vaqtincha ishlamayapti.':
      'Akkaunt tasdiqlanmadi. Parol, tanlangan akkaunt yoki tasdiq muddatini tekshiring.');
    return await response.json();
  }finally{clearTimeout(timer);}
}
function acceptProof(data){
  if(typeof data.request_id!=='string'||!/^daw_[A-Za-z0-9_-]{39}$/.test(data.request_id)||
     typeof data.proof!=='string'||!/^[A-Za-z0-9_-]{43}$/.test(data.proof)||data.expires_in_seconds!==300)
    throw new Error('Xizmat javobi tasdiqlanmadi.');
  proof={request_id:data.request_id,proof:data.proof};
  el('confirm-form').hidden=false; status('Akkaunt tekshirildi; o‘chirish uchun DELETE deb yozing.');
  el('confirmation').focus();
}
async function perform(action){
  if(busy||!available)return;
  busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);
  status('So‘rov bajarilmoqda…');
  try{await action();}catch(error){status(error.name==='AbortError'?
    'Javob kelmadi. O‘chirish natijasi noaniq bo‘lsa, shu oynada qayta urinib ko‘ring.':error.message);}
  finally{busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=!available);}
}
function b64(bytes){return btoa(String.fromCharCode(...bytes)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
el('google-button').addEventListener('click',()=>perform(async()=>{
  const verifier=b64(crypto.getRandomValues(new Uint8Array(48)));
  const challenge=b64(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(verifier))));
  const data=await api('/account/deletion/web/google',{code_challenge:challenge});
  const url=new URL(data.auth_url);
  if(url.protocol!=='https:'||url.hostname!=='accounts.google.com'||url.username||url.password||url.hash||
     typeof data.state!=='string'||!data.state.startsWith('del_')||url.searchParams.get('state')!==data.state)
    throw new Error('Google manzili tasdiqlanmadi.');
  sessionStorage.setItem('ilm-deletion-reauth',JSON.stringify({verifier,state:data.state,expires:Date.now()+600000}));
  location.assign(url.href);
}));
el('password-form').addEventListener('submit',event=>{
  event.preventDefault();perform(async()=>{
    try{acceptProof(await api('/account/deletion/web/password',{email:el('email').value.trim(),password:el('password').value}));}
    finally{el('password').value='';}
  });
});
el('confirm-form').addEventListener('submit',event=>{
  event.preventDefault();perform(async()=>{
    if(!proof||el('confirmation').value!=='DELETE')throw new Error('Avval akkauntni qayta tasdiqlang.');
    const result=await api('/account/deletion/reauth/confirm',{...proof,confirmation:'DELETE'});
    if(!['deleted','pending_cleanup','retention_review'].includes(result.state)||
        result.account_revoked!==(result.state!=='retention_review'))throw new Error('O‘chirish natijasi tasdiqlanmadi.');
    if(result.state==='deleted'){
      status('Akkaunt va unga tegishli ma’lumotlar o‘chirildi.');proof=null;
      el('confirm-form').hidden=true;el('password-form').reset();
    }else if(result.state==='pending_cleanup')status('Akkaunt yopildi. Fayllarni tozalash hali tugamadi; shu tasdiq bilan qayta tekshirishingiz mumkin.');
    else status('So‘rov moliyaviy saqlash tekshiruviga yuborildi; akkaunt hali o‘chirilmagan.');
  });
});
el('manual-form').addEventListener('submit',event=>{
  event.preventDefault();perform(async()=>{
    const result=await api('/account/deletion/manual-request',{
      account_email:el('account-email').value.trim(),contact_email:el('contact-email').value.trim(),reason:el('reason').value.trim()});
    if(result.state!=='pending_identity_review'||result.account_deleted!==false||
      !/^[A-Za-z0-9_-]{43}$/.test(result.request_id))throw new Error('So‘rov qabul qilingani tasdiqlanmadi.');
    status('So‘rov saqlandi. Shaxsni alohida tekshirish talab qilinadi; akkaunt o‘chirilmagan. So‘rov raqami: '+result.request_id);
    el('manual-form').reset();
  });
});
(async()=>{
  const callback=new URLSearchParams(location.hash.slice(1));
  if(location.hash)history.replaceState(null,'','/account-deletion');
  try{
    const config=await api('/account/deletion/config');
    available=config.available===true&&config.email_required===false;
    document.querySelectorAll('button').forEach(b=>b.disabled=!available);
    if(!available){status('O‘chirish xizmati hali tayyor emas. Keyinroq qayta urinib ko‘ring.');return;}
    if(callback.has('state')){
      const saved=JSON.parse(sessionStorage.getItem('ilm-deletion-reauth')||'null');
      sessionStorage.removeItem('ilm-deletion-reauth');
      if(!saved||Date.now()>saved.expires||callback.getAll('state').length!==1||callback.get('state')!==saved.state||
         callback.has('error')||callback.getAll('code').length!==1||!/^[A-Za-z0-9_-]{43}$/.test(callback.get('code')))
        throw new Error('Google qayta tasdiqlashi bajarilmadi; qayta urinib ko‘ring.');
      await perform(async()=>acceptProof(await api('/account/deletion/reauth/exchange',{code:callback.get('code'),code_verifier:saved.verifier})));
    }
  }catch(error){status(error.message);}
})();
