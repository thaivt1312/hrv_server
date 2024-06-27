import { useEffect, useState } from "react";
import Router from "./router";
import { requestForToken, onMessageListener } from "./firebase";

import { ToastContainer, toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

import { Stack, Button } from "@mui/material";
import Navbar from "./components/NavBar";


function App() {
  const [hasPermission, setHasPermission] = useState(false)
  const [notiList, setNotiList] = useState(localStorage.getItem('notiList') ? JSON.parse(localStorage.getItem('notiList')) : [])

  function requestPermission() {
    console.log('Requesting permission...');
    Notification.requestPermission().then((permission) => {
      if (permission === 'granted') {
        console.log('Notification permission granted.');
        setHasPermission(true)
      }
    })
  }
  useEffect(() => {
    requestPermission()
    async function fetchToken() {
      let token = await requestForToken()
      localStorage.setItem('firebaseToken', token)
    }
    fetchToken()
  }, [])

  onMessageListener().then(payload => {
    // setNotification({title: payload.notification.title, body: payload.notification.body})
    // setShow(true);
    console.log(payload)
    let arr = [...notiList]
    arr.push(payload?.data?.data)
    setNotiList([...arr])
    localStorage.setItem('notiList', JSON.stringify(arr))
    toast(payload?.data?.data)
  }).catch(err => console.log('failed: ', err));

  const clearNotiList = () => {
    setNotiList([])
    localStorage.removeItem('notiList')
  }

  return (
    <>
      <div style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
      }}>
        {
          !hasPermission ?
            <span style={{ color: 'red' }}>Please allow notification permission</span>
            : <></>
        }
        <Navbar />
        <Stack direction={"row"} sx={{ width: '100vw', height: '90vh' }}>
          <div style={{
            width: '80vw',
            minHeight: '60vh',
            maxHeight: '90vh',
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
          }}>
            <Router />
          </div>

          <Stack sx={{ border: 'solid 1px', width: '20vw', height: '90vh' }}>
            <Button sx={{ border: 'solid 1px' }} onClick={clearNotiList}>
              Clear notifications list
            </Button>
            {
              notiList.map((noti) => {
                return (
                  <Stack sx={{ border: 'solid 1px' }}>
                    {noti}
                  </Stack>
                )
              })
            }
          </Stack>

        </Stack>
        <ToastContainer />

      </div>
    </>
  )
}

export default App
