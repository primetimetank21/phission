import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Text, VStack, useColorMode} from "@chakra-ui/react"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"display_email_message_subjects": false, "display_score": false, "email_message_subjects": [], "email_messages": [], "email_panel_state": {"button_bg_color": "green", "text_color": "black"}, "get_risk_str": "somewhat safe", "ipqs": {}, "number_of_email_messages": 0, "risk_score": null, "url": "", "url_display": "", "user_email": "jhnwck2023@gmail.com", "user_password": "password123EZ", "events": [{"name": "state.hydrate"}]})
const [result, setResult] = useState({"state": null, "events": [], "processing": false})
const router = useRouter()
const socket = useRef(null)
const { isReady } = router;
const { colorMode, toggleColorMode } = useColorMode()
const Event = events => setState({
  ...state,
  events: [...state.events, ...events],
})
useEffect(() => {
  if(!isReady) {
    return;
  }
  if (!socket.current) {
    connect(socket, state, setState, result, setResult, router, EVENT, ['websocket', 'polling'])
  }
  const update = async () => {
    if (result.state != null) {
      setState({
        ...result.state,
        events: [...state.events, ...result.events],
      })
      setResult({
        state: null,
        events: [],
        processing: false,
      })
    }
    await updateState(state, setState, result, setResult, router, socket.current)
  }
  update()
})
return (
<VStack justifyContent="center"
alignItems="center"
sx={{"display": "flex"}}><Text>{`Google <no-reply@accounts.google.com>`}</Text>
<Text>{`jhnwck2023@gmail.com`}</Text>
<Text>{`Thu, 02 Mar 2023 22:27:55 GMT`}</Text>
<Text>{`Security alert`}</Text>
<Text>{`[image: Google] 
A new sign-in on Linux 
 
 
jhnwck2023@gmail.com 
We noticed a new sign-in to your Google Account on a Linux device. If this 
was you, you don’t need to do anything. If not, we’ll help you secure your 
account. 
Check activity 
<https://accounts.google.com/AccountChooser?Email=jhnwck2023@gmail.com&continue=https://myaccount.google.com/alert/nt/1677796075252?rfn%3D325%26rfnc%3D1%26eid%3D2286003474807739465%26et%3D0> 
You can also see security activity at 
https://myaccount.google.com/notifications 
You received this email to let you know about important changes to your 
Google Account and services. 
© 2023 Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA 
`}</Text>
<Text>{`["https://accounts.google.com/AccountChooser?Email=jhnwck2023@gmail.com&continue=https://myaccount.google.com/alert/nt/1677796075252?rfn%3D325%26rfnc%3D1%26eid%3D2286003474807739465%26et%3D0", "https://myaccount.google.com/notifications"]`}</Text>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta content="favicon.ico"
property="og:image"/></NextHead></VStack>
)
}