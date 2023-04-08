import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Alert, AlertTitle, Button, Center, Container, Heading, Input, Text, VStack, useColorMode} from "@chakra-ui/react"
import {CheckCircleIcon, QuestionIcon, WarningTwoIcon} from "@chakra-ui/icons"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"display_score": false, "get_risk_str": "somewhat safe", "ipqs": {}, "risk_score": null, "url": "", "url_display": "", "events": [{"name": "state.hydrate"}]})
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
<Center sx={{"height": "100vh", "width": "auto", "bg": "#0051a8"}}><VStack spacing="1.5em"
sx={{"fontSize": "2em"}}><Heading sx={{"fontSize": "2em"}}>{`Welcome to Phissi👁️n!`}</Heading>
{state.display_score ? (state.risk_score >= 75) ? (state.risk_score >= 85) ? <Alert status="error"
sx={{"bg": "#0051a8"}}><WarningTwoIcon/>
<AlertTitle sx={{"color": "white"}}>{(((((("\"" + state.url_display) + "\" is a ") + state.get_risk_str) + " website! (score: ") + state.risk_score) + ")")}</AlertTitle></Alert> : <Alert status="error"
sx={{"bg": "#0051a8"}}><QuestionIcon/>
<AlertTitle sx={{"color": "white"}}>{(((((("\"" + state.url_display) + "\" is a ") + state.get_risk_str) + " website! (score: ") + state.risk_score) + ")")}</AlertTitle></Alert> : <Alert status="error"
sx={{"bg": "#0051a8"}}><CheckCircleIcon/>
<AlertTitle sx={{"color": "white"}}>{(((((("\"" + state.url_display) + "\" is a ") + state.get_risk_str) + " website! (score: ") + state.risk_score) + ")")}</AlertTitle></Alert> : <Text sx={{"color": "white"}}>{`Type a URL`}</Text>}
<Container sx={{"borderBottom": "0.5px solid grey", "height": "45px"}}><Input placeholder="Url to test (i.e., google.com)"
type="text"
focusBorderColor="None"
onBlur={(_e) => Event([E("state.set_url", {value:_e.target.value})])}
sx={{"border": "0px", "focusBorderColor": "None", "color": "white", "fontWeight": "semibold"}}/></Container>
<Button colorScheme="green"
onClick={() => Event([E("state.set_IPQS", {})])}>{`Go Phish`}</Button></VStack>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta property="og:image"
content="favicon.ico"/></NextHead></Center>
)
}