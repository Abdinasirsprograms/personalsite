<template>
<div>
  <input type="url" v-model="payload.site_url" @keyup.enter="send_payload()">
  <!-- <input type="text" v-model="payload.site_url" @keyup.enter="getData(payload)"> -->
  <br>
  <div>
  </div>
  <button v-if ="connected || recieved_html_response" @click="close_connection()">Close connection</button>
  <button v-else  @click="send_payload()">+ Add website</button>
  <div v-if="recieved_html_response">
    <h1>Message recieved from server : </h1>
    <div v-html="recieved_html_response"></div>
    <br>
    <br>
    <br>
  </div>
</div>
</template>


<script setup lang="ts">

import { ref, reactive, onMounted, computed } from 'vue'


const payload = reactive({
    site_url: '',
})

let recieved_html_response = ref('')
const webSocketObject = () => {
  return new WebSocket('ws://localhost:80/newsreader')}
let init = ref(false)
let connected = ref(false)
const safe_word = 'CLOSE_CONNECTION' 

const close_connection = () => {
    send_message(safe_word)
}
  
const send_message = (message: string) => {
    if(connected.value){return}
    const webSocket = webSocketObject()
    webSocket.onopen = () => {
      connected.value = true
      if(message === safe_word){webSocket.close();return}
      webSocket.send(message)
    }
    webSocket.onclose = () => {
      connected.value = false
      payload.site_url = ''
    }
    webSocket.onmessage = ({data}) => {
      parseResponseHTML(data)
      payload.site_url = ''
    }
}

const parseResponseHTML = (data) => {
    // const currentHead = document.querySelector('head').outerHTML
    // const el = document.querySelector('#app')
    // let parsedHead = currentHead.slice(currentHead.indexOf('>')+1, currentHead.length)
    // parsedHead = currentHead.slice(currentHead.length - currentHead.indexOf('</h'), currentHead.indexOf('</h'))
    // parsedHead = parsedHead.trim()
    // const responseData = new DOMParser().parseFromString(data, 'text/html')
    // responseData.querySelector('head').querySelectorAll('meta').forEach((e) => e.remove())
    // responseData.querySelector('head').querySelectorAll('title').forEach((e) => e.remove())
    // let combinedHead = parsedHead + responseData.querySelector('head').outerHTML 
    // responseData.querySelector('body').prepend(el)
    // let combinedHTML = combinedHead + responseData.querySelector('body').outerHTML
    // console.log(combinedHTML)
    const responseData = new DOMParser().parseFromString(data, 'text/html')
    data = responseData.querySelector('body').outerHTML
    recieved_html_response.value = data
    // document.querySelector('html').appendChild(responseData)

}

const parsedSiteUrl = computed(() => {
  let siteURL = payload.site_url
  if (siteURL !== ''){
    siteURL = siteURL.indexOf('https://') === -1 ? 'https://' + siteURL : siteURL
    siteURL = siteURL.indexOf('.com') === -1 ? siteURL + '.com/' : siteURL 
    return siteURL
  }
  else {
    return false
  }
})

const send_payload = () => {
  if(!parsedSiteUrl.value){return}
  send_message(parsedSiteUrl.value)
}




/*

import axios, { AxiosRequestConfig, AxiosResponse } from 'axios'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'HTTP_X_CSRFTOKEN'


const cookie = document.cookie
const optionalHeaders = {'X-CSRFToken':'',
'content-type':'text/html',}

const cookieSearchTerm = cookie.indexOf('csrftoken=')
const CSRF_TOKEN = cookie.substring(cookieSearchTerm).split('csrftoken=')[1]

if (cookieSearchTerm >= 0){
  optionalHeaders['X-CSRFToken'] = `${CSRF_TOKEN}`
  optionalHeaders['content-type'] = 'application/json'
  optionalHeaders['redirect'] = 'allow'
} else {
  throw new Error("Token not established")
}





    // const sitePOSTconfig: AxiosRequestConfig = {
    //     baseURL: 'http://localhost:80/projects/newsreader',
    //     url: '/submit-url',
    //     method: 'post',
    //     headers: {...optionalHeaders},  
    //     xsrfCookieName: 'csrftoken',
    //     xsrfHeaderName: 'HTTP_X_CSRFTOKEN',
    //     timeout: 5000,
        
    // }

    // async function getData(payload: any){
    //   loading_state.value = true
    //   const dataResponse = await axios.post('http://localhost:80/projects/newsreader/submit-url', payload, sitePOSTconfig)
    //   .then(data => {
    //     const currentHead = document.querySelector('head').outerHTML
    //     const el = document.querySelector('#app')
    //     let parsedHead = currentHead.slice(currentHead.indexOf('>')+1, currentHead.length)
    //     parsedHead = currentHead.slice(currentHead.length - currentHead.indexOf('</h'), currentHead.indexOf('</h'))
    //     parsedHead = parsedHead.trim()
    //     const responseData = new DOMParser().parseFromString(data.data, 'text/html')
    //     responseData.querySelector('head').querySelectorAll('meta').forEach((e) => e.remove())
    //     responseData.querySelector('head').querySelectorAll('title').forEach((e) => e.remove())
        
    //     let combinedHead = parsedHead + responseData.querySelector('head').outerHTML 
    //     responseData.querySelector('body').prepend(el)
    //     let combinedHTML = combinedHead + responseData.querySelector('body').outerHTML
    //     console.log(combinedHTML)
    //     document.querySelector('html').innerHTML = combinedHTML
    //     })
    //   .catch((err) => {recieved_html_response.value = err})
    // }

*/



</script>


<style scoped>
a {
  color: #42b983;
}

label {
  margin: 0 0.5em;
  font-weight: bold;
}

code {
  background-color: #eee;
  padding: 2px 4px;
  border-radius: 4px;
  color: #304455;
}
.animate_load_state::before {
  position: absolute;
  content: "⌛";
  opacity: 0;
  animation: 750ms clock_animation_show 100ms ease-in-out alternate infinite;
}

@keyframes clock_animation_show {
  100% {
    opacity: 1;
  }
}
</style>
