<template>
<div>
  <input type="text" v-model="payload.site_url" @keyup.enter="getData(payload)">
  <br>
</div>
</template>


<script setup lang="ts">
import { reactive } from 'vue'
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'HTTP_X_CSRFTOKEN'

const payload: { site_url: string; } = reactive({
    site_url: '',
})

const cookie = document.cookie
const optionalHeaders = {'X-CSRFToken':'',
'content-type':'',}

const cookieSearchTerm = cookie.indexOf('csrftoken=')
const CSRF_TOKEN = cookie.substring(cookieSearchTerm).split('csrftoken=')[1]

if (cookieSearchTerm >= 0){
  optionalHeaders['X-CSRFToken'] = `${CSRF_TOKEN}`
  optionalHeaders['content-type'] = 'application/json'
} else {
  throw new Error("Token not established")
}

const sitePOSTconfig: AxiosRequestConfig = {
    baseURL: 'http://localhost:80/projects/newsreader',
    url: '/submit-url',
    method: 'post',
    headers: {...optionalHeaders},  
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'HTTP_X_CSRFTOKEN',
    timeout: 1500,
    
}

function getData(payload: any){
  console.warn(payload)
  const dataResponse = axios.post('http://localhost:80/projects/newsreader/submit-url', payload, sitePOSTconfig)
  .then((res) => {return res.data}).catch((err) => {return err})
  const cleanedRes = handleResponse(dataResponse)
}

async function handleResponse(data: Promise<AxiosResponse<any, any>>){
  console.log('this is what\'s recieved:', await data)
  return data
}


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
</style>
