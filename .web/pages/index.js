import {useEffect, useRef, useState} from "react"
import {useRouter} from "next/router"
import {E, connect, updateState} from "/utils/state"
import "focus-visible/dist/focus-visible"
import {Alert, AlertIcon, AlertTitle, Button, Center, Heading, Input, VStack, useColorMode} from "@chakra-ui/react"
import NextHead from "next/head"

const EVENT = "ws://localhost:8000/event"
export default function Component() {
const [state, setState] = useState({"risk_score": 92, "search_text": "", "url": "goalgoof.com", "events": [{"name": "state.hydrate"}]})
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
<Center sx={{"paddingTop": "10%"}}><VStack spacing="1.5em"
sx={{"fontSize": "2em"}}><Alert status="error"><AlertIcon/>
<AlertTitle>{(((("\"" + state.url) + "\" is a risky website! (score: ") + state.risk_score) + ")")}</AlertTitle></Alert>
<Heading sx={{"fontSize": "2em"}}>{`Welcome to Phissi👁️n!`}</Heading>
<Input type="text"
placeholder="Url to test (i.e., google.com)"
onBlur={(_e) => Event([E("state.set_search_text", {value:_e.target.value})])}/>
<Button colorScheme="green">{`Go Phish`}</Button></VStack>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta property="og:image"
content="favicon.ico"/></NextHead></Center>
)
}