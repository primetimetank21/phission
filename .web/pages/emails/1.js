import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Text, VStack, useColorMode} from "@chakra-ui/react"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"display_score": false, "email_messages": [], "email_panel_state": {"button_color_scheme": "green", "display_email_message_subjects": false, "email_message_subjects": [], "number_of_email_messages": 0, "text_color": "black"}, "get_risk_str": "somewhat safe", "ipqs": {}, "risk_score": null, "url": "", "url_display": "", "user_email": "jhnwck2023@gmail.com", "user_password": "password123EZ", "events": [{"name": "state.hydrate"}]})
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
sx={{"display": "flex"}}><Text>{`Elana <mail@thesocialman.com>`}</Text>
<Text>{`jhnwck2023@gmail.com`}</Text>
<Text>{`Mon, 13 Mar 2023 15:45:41 -0400`}</Text>
<Text>{`Is This Guy a Loser, Or Not? (Plus a Warning)`}</Text>
<Text>{` 
 
 
This email was sent to jhnwck2023@gmail.com by mail@thesocialman.com 
Manage Subscriptions 
https://links.herocomail.com/a/325/unsubscribe/3172779/743348217/f6bacdc20602e8a308481fad6e8aa838bbd45c86 
100 Congress Ave, Suite 2000 Austin, TX 78701 
 
`}</Text>
<Text>{`["https://links.herocomail.com/a/325/unsubscribe/3172779/743348217/f6bacdc20602e8a308481fad6e8aa838bbd45c86"]`}</Text>
<NextHead><title>{`Pynecone App`}</title>
<meta name="description"
content="A Pynecone app."/>
<meta content="favicon.ico"
property="og:image"/></NextHead></VStack>
)
}