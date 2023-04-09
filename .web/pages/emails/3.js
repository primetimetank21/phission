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
<VStack alignItems="center"
justifyContent="center"
sx={{"display": "flex"}}><Text>{`Christian Hudson <mail@thesocialman.com>`}</Text>
<Text>{`jhnwck2023@gmail.com`}</Text>
<Text>{`Sun, 12 Mar 2023 14:38:01 -0400`}</Text>
<Text>{`Re: What women want quiz answers`}</Text>
<Text>{`I actually threw up the first time I made a cold call for a startup I was trying to launch.  
  
Thanks to my social anxiety… Nearly every kind of social situation made me so uncomfortable and nervous that I’d get nauseous.   
  
Small talk with people I didn’t know would make my mind race... my palms sweat... and my heart pound like a jackhammer.   
  
And making friends, or starting relationships… forget it. I made up a bunch of excuses for why I was “too busy” or “not ready” for them.  
  
Back then, I didn’t want to accept how much my social anxiety was holding me back in life.  
  
But life was passing me by… one missed social opportunity at a time.  
  
- Job raises and promotions…  
- Trips, festivals, and adventures with friends…  
- Doors opening to new business ventures and connections…  
- Maybe finding a girl to settle down with…  
  
NONE of that was within my reach back then, thanks to my social anxiety.  
  
If you can relate… You’re going to love what I’ve got for you.  
  
You see, those days are long gone.   
  
As a coach of mine once told me, “Confidence Is Predictable Results”.   
  
You can’t just look at yourself in a mirror and talk yourself into being more confident.  
  
Obviously, if you could you that, you would have done it already.  
  
But…  
  
If you knew that you could enter a social situation, and PREDICTABLY get good results - every time - it’d give you a lot of confidence, wouldn’t it?  
  
That’s exactly what these three “master switches” are for.   
  
They’re on THIS page, waiting for you to download them.  
  
You’ll create a “reality distortion field” in social interactions…  
  
The same kind of field that men like Bill Clinton, Steve Jobs, and Elon Musk create every time they speak…  
  
And social anxiety will be a thing of the past for you.  
  
So the women you want to date, the experiences you want to have, the career growth you’ve been dying for… That all opens up to you, almost immediately.  
  
When you Download the 3 master switches HERE, you’ll also get my top 3 tips for becoming instantly likable to people - to men, and especially to women.  
  
(Hint: It’s not about what YOU say… It’s about what you get OTHERS to say)  
  
Write back to me, and let me know how the switches go for you!  
  
Rock and Roll,  
Christian  
  
  
This email was sent to jhnwck2023@gmail.com by mail@thesocialman.com  
Manage Subscriptions  
https://link.thesocialman.com/a/325/unsubscribe/9708530/743348217/262926c677aefe7502121675dea1bc385a36775c  
100 Congress Ave, Suite 2000 Austin, TX 78701  
  
`}</Text>
<Text>{`["https://link.thesocialman.com/a/325/unsubscribe/9708530/743348217/262926c677aefe7502121675dea1bc385a36775c"]`}</Text>
<NextHead><title>{`Pynecone App`}</title>
<meta name="description"
content="A Pynecone app."/>
<meta property="og:image"
content="favicon.ico"/></NextHead></VStack>
)
}