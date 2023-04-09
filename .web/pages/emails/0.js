import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Text, VStack, useColorMode} from "@chakra-ui/react"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"display_score": false, "email_messages": [], "email_panel_state": {"button_bg_color": "green", "display_email_message_subjects": false, "email_message_subjects": [], "number_of_email_messages": 0, "text_color": "black"}, "get_risk_str": "somewhat safe", "ipqs": {}, "risk_score": null, "url": "", "url_display": "", "user_email": "jhnwck2023@gmail.com", "user_password": "password123EZ", "events": [{"name": "state.hydrate"}]})
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
<VStack alignItems="center"
justifyContent="center"
sx={{"display": "flex"}}><Text>{`"T.S.M.D." <mail@thesocialman.com>`}</Text>
<Text>{`jhnwck2023@gmail.com`}</Text>
<Text>{`Tue, 14 Mar 2023 21:04:02 -0400`}</Text>
<Text>{`THIS is what women are really looking for in a man... And it's simpler and weirder than you've ever thought.`}</Text>
<Text>{` 
 
 
This email was sent to jhnwck2023@gmail.com by mail@thesocialman.com 
Manage Subscriptions 
https://link.thesocialman.com/a/325/unsubscribe/9950699/743348217/95ac0f0997da31d7dce49b4818407872dd872cc4 
100 Congress Ave, Suite 2000 Austin, TX 78701 
 
`}</Text>
<Text>{`["https://link.thesocialman.com/a/325/unsubscribe/9950699/743348217/95ac0f0997da31d7dce49b4818407872dd872cc4"]`}</Text>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta content="favicon.ico"
property="og:image"/></NextHead></VStack>
)
}