---
layout: default
lang: fr
alt: /subscribed/
title: Inscription confirmée
permalink: /fr/subscribed/
---

# Inscription confirmée
{:.no_toc}

Merci. Votre inscription est confirmée. Le prochain courriel arrivera au rythme choisi : chaque nouvelle étude le matin, le lundi, ou le 1er du mois. Chaque message se termine par un lien de désinscription en un clic.
{:.lead}

[Retour à la revue](/fr/)

<div id="sub-state" class="lead" data-api="{{ site.subscribe_api }}" data-action="confirm" data-lang="fr" hidden></div>
<script>
(function(){var box=document.getElementById('sub-state');var t=new URLSearchParams(location.search).get('t');if(!t||!box.dataset.api)return;
  var fr=box.dataset.lang==='fr';var lead=document.querySelector('.lead:not(#sub-state)');if(lead)lead.hidden=true;box.hidden=false;
  box.textContent=fr?'Un instant…':'One moment…';
  fetch(box.dataset.api+'?action='+box.dataset.action+'&t='+encodeURIComponent(t)+'&json=1',{credentials:'omit',redirect:'follow'})
   .then(function(r){return r.json();}).then(function(j){
     if(j.ok&&box.dataset.action==='confirm'){box.textContent=fr?'Merci. Votre inscription est confirmée. Le prochain courriel arrivera au rythme choisi ; chaque message se termine par un lien de désinscription en un clic.':'Thank you. Your subscription is confirmed. The next email comes at the rhythm you chose; every message ends with a one-click unsubscribe link.';}
     else if(j.ok){box.textContent=fr?'Désinscription effectuée. Vous ne recevrez plus de courriels de la revue vivante.':'You are unsubscribed. You will receive no more emails from the living review.';}
     else{box.textContent=fr?'Lien inconnu ou expiré. Réinscrivez-vous depuis la page Courriel, ou écrivez à a.p.joly@lse.ac.uk.':'Unknown or expired link. Sign up again from the Email page, or write to a.p.joly@lse.ac.uk.';}
   }).catch(function(){box.textContent=fr?'Le serveur ne répond pas ; réessayez dans un instant.':'The server did not answer; please try again in a moment.';});})();
</script>
