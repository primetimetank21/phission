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
sx={{"display": "flex"}}><Text>{`Google Community Team <googlecommunityteam-noreply@google.com>`}</Text>
<Text>{`jhnwck2023@gmail.com`}</Text>
<Text>{`Wed, 08 Feb 2023 13:29:15 -0800`}</Text>
<Text>{`Take the next step by customizing your Google Account`}</Text>
<Text>{` 
Let's get started! 
Welcome to Google. Your new account comes with access to Google products,   
apps, and services. Here are a few tips to get you started. 
 
Get personalized tips, news, and recommendations for Google products and   
services<https://notifications.google.com/g/p/APdRdFwgyeD2Ig8ZEIVz1e2l9QTOPqMd2OzB9zfFli8u-rARJgIOKiDToT0aZab3QV_5ppf6ZEYPqqA8dxrT2DWQ2_2eAihP_j33IzVU4HeeZ2zfu-gRDAFG50VAcoXRjDPhiWOIcnSbXDgW5yyswynXazhz83NDXRoemoFrVbrNpwF8_QRdXhiypGaNHFh25JJuzft2d3qrSzHKxTaWmULf9WJEn8SjU43m4d2h248cDXGythFbsGrw8MdrfkbJ1ojgCwSdIQ-xE2o_6VLExeJp_1A6ajKxRUvyO2h1OHynxWGwBi5kJWhOiuZ5guhjKLTQ3rY834Swj7rhacW9ia1P35jpgKljW0jaTp1NSUmNosHkiChfU9qnTArhK8x7wZOoA0JYPczrPqeP2782iJqaHCoMEuw2gaqGEdZb0XRMWfPh0Y_T5-1ij46NxV0wYlu3QLn65JZCUWEoIK73CKmfsHBaRLgKRRd4cTYL2qhgOBrdtI_BwEqveVXdLY3lQXAntEZn8_THZsiW0LAVcsR2MYwxWwemkJLY5ShuaKIlOwMDYMNxuSfGO7mOAPy8> 
Get the most out of your Google Account 
We'll send you personalized tips, news, and recommendations from Google. 
Yes, keep me   
updated<https://notifications.google.com/g/p/APdRdFwjttxARUhGfC0tURqJYGzO_xe_yyQhBsiS8qv7Zo-ijssQFqfcPKj04Zrn4Mik0Ct7eXslFoKA8IrNQ94jMCMAoTg7CGuxRi1rsx9AjG2r4skv62DnBfZYRLUMY5yUrxb47lB03e3ppa8kB1o_afAvrBVElR7XZZaClzHiGo8mzAJ_yuohewXJwYj9K6aAdtDGUzK--ADb07gvQhzUNvZEyNtNKKMvzrNwEfJfMl4n6zw-41LW-Nck0LKHzv-uM8cILGMVsDFLCMm6RdPBkp01-w9lmInxDeDxEQ8uOPSrFmzMWBqrD9GJlH6Ei7BTjL-NO7MgIb4BX8bgSxUg4Rq_WeY_7V-s6_f3vfFn2TnTQeXgBHVbDHPgWeqdlmfBK96LCfNoZ7KpdG9Iu_7lTznBXiucT9lMLVaGIsd5g_6_6MXXvu--_6Eft41HIDQfRD8fnGl81yyOZwHSgZ7_Dp3lRqWt5A_8qIOPxBejOOWGNuwuHzbDN_-h3GwkRaGYIkFwpHdFO8j2dfYiDxeYgep19JWZjKSa3Wt-B88ibdyRabayU-CjcSv1oamROg> 
 
Try the Google app to find answers and information   
quickly<https://notifications.google.com/g/p/APdRdFyJivR-gBYMRsTTiyCsL_n6Iaz3ntNt_fycfiNvpvFAvIYCbskE7nv8gf2qoT4bAjmWEy7j5msOmAnEhrbvXd4OhQ31CdQcOLnoXN8AlAgbsu5bCupe-WRW3EVkBaFHePbExbcfSuxrkvPE9_MIkdZJOh-sY0Il34GKXh0iVzy3rVvT7nczoFHCd9GO06TGoDZ2c4YQ3pb2gMoKHKbInvvqPm0GYAg1xDVHUIPMvaYtwUi32BaO1PYQZN8VtAU-H18AAIk0bsNz3Td7YZz4Pu8ek5Nrgb1vJ8MlczpErIHH4Kmfj24je-kDdtDuOvE0I-Brw8-ma3qm4dpVMu6vLREtadtRHhtn2Q> 
Stay in the know with the Google app 
  Find quick answers, explore your interests, and stay up to date. 
Try   
it<https://notifications.google.com/g/p/APdRdFweHsW4rIQeiA4qmrZ61liWOwXABmkkuxpKnMB2OnGtCe75r8fP1hKe9yfp-hdUdLwkEWKS9oVoiUMc8EPaqHLVVlJcQcEHd_ha5aGra7zla06dhw-JRGpKhXTpK6wD6aOa2zfECZL606UgVmZrS64yjc3paW754WdObXTe2HbyIGo3RueEc9rjuXXo8Ea7EtAJvJFod0lahWEFwF4FK4UFMUAJpKGLm6eTef3XZCNZ1z1yHNJSiY77IAv-Od_qxDkcHn_7Nvcc7e2Qi25Xi4GE6C7yZesjbh7vb3Gj6LZvTUZtwo8rg0eGadRyufwxtqqpaiT3FXTyXrDgdVYJNDKsTgmYbF8Razg> 
 
Explore apps to use Google products and services across   
devices<https://notifications.google.com/g/p/APdRdFy_grULWqj0r7KicKvQmLN-oxB-tvnTTvwMQCcw2_PYH9nzzpnLiB9WQYoXi-VWXbOnmrAM7ymRHt7iX5qspSHXEbNdycNOeJMbRkg9AduXcbtDW_eTr5V6EBxcb6MIP0F6gZ9j_Dale6oufq5uCpRqBt07qSzxFu_pHP-_TRfTOgbAVQfCj_zNDyR8B7RLD3u04BDZaW0nZlqNtk6E5E8RMiif7wPpX7vR9eEx4n_tCAKphO1kf0rH1a3Kqg7s1iYWiADRSWh3wpURgCJs-H8SRy-e_SFbuF3DHiJoFwZQME6Oft3aTsbXqxKMaCBTdpx1tnkSjTI18H-uyiq7yoISHARyJC0-k5qBWv-Jy0PgbhghdB5fz9Jw0k1Ac9eHhHabZuFjqB4NsuIX2-MABxyV6n6RZ7LhTGVMZqMcZapiqiwrPY7PSZUGxUTsRCulPTBO-PvFi2_QR2Ha6GisIarIDpD9E9r8a9vvWOHFnI0oOs4GKF8w5dT1Yf_WJHEgapDas2Ks2Hm4fDDkqMoIrIjkhL4JbMHMQlXG2RlTVIkfNC4zYXCMcIcoHHNZojXIr7srZw0ygtGuXJAuod-fyJ3n5yi5-8KrqhvemJs_6byAhk5KMNOj5gg1OtoVeMKa_zG9Fpa8sG8> 
More from Google 
Discover the latest apps from Google. 
For   
Android<https://notifications.google.com/g/p/APdRdFxX28ST_hbbTvnhyA3oQj7biSk2GAMJW_yeAIGQgZFNYD3cPSLJ1ffsomTwxRz7sDmVigct8rmhmwkLIGbL9TU8-FwA6aRjkTXjg4u0mVkEeu1ANnBySv4S0oftPy-bjd10qsSpWoYGbSiyNaUAd1J8LMmBK6q2eXGhxVokitEBEET-ApzNUsoGxge_ZWgHHFrnuoeogKMGVNZ-_cLR9O2Cwe9NAKlox5NlzboYQ2eljjkYtMLrpg0QdWQ62Hm1cZe8XGS0EC_8-UySHBIC1ks3FBEjfOkNNzQm07I-L9VVXWxONZG76DvFzNup0DpApaiDv1BprE_TsiXhV9WDQc2fDtbMjdR8m4fCePqgVFBjAhu8Um4TfzqlXJCh-btjy3nCU6ejYWLFmobDrANQXW5BCYfdSFWs7SkmE4qcXJ8YvXpqVWRhTNAQw4cGNnCGBTOmwsG9uhxc5FPAYXuALMn9W7sGl8GRxHyzUdAdnERGx88aG-wKuQD--2vyc97-0MpOKSGiNASVd7IEUcEUgTzZVYFKIhFXWym6h-acs_CxdCtuRqAr09pGaIJjh0-OMvKzqRwl2-5ozhTnDn88r1oA-zfEtYGZHBpF3u9VJW87k8QMUjxJYBw0sqLMPLEQwXRPlSWuXwFF> 
For   
iOS<https://notifications.google.com/g/p/APdRdFz_itmsd2WLHTg8K8W3eePq3eYaS01UJQm_Q9VT6EDFdIj665CUMq0AKpv9-mE4ZvlYVy6iaXbrX12qgUsHTuW39Z1iePDcAoXmxMZWt14b8yJIRCbkVPmvDdxnwjQ3i-YEPkG4fQxvqq8ya8g3BwfqJeinmItqcnWXZAOHfBIFN_WxgxPP0alY4z450L9HdSjYEMdriD38P1D5338Mc37l0OqIMAtKtkgBeLC1AWO995GVGrFGJ3oa4eTjccna6OA6-I4J8fVOtMrMq6Xe1IbU79sCJjkFXrGT_Xe1sA11QBuWQ0PSTXa-A7iJOnYnDrEhlxAVy8bTqT-JyQPDil0tMfx1vpuYqpn7xl7wRx2QfZOp_16Vs7GWTQ> 
 
Customize your privacy and security   
settings<https://notifications.google.com/g/p/APdRdFwC8mXc5tBPUptckZzVjJq_97JIevAlxCHBUSXnWkrePa66dbGC4WdPIB4KxNDDxc-45FOTPLaNCAepf6oCFWXkqj3GRvZw_gjsAeINLdlWo8Psv3cE_23YKhWaXw3Rm_HW_CAogd_2Et-8aRHgcA7Qgl72HYTdXDq1EIpXF9gN2MnrA_tLnI-OflvpEWo_NwmWA5SzT4BbAJOAkxkiDgov86MsxnUKUG6pM6eKbBtZzEKpqjsE3_5tcPYXxLNVzOjqHdoG2VxOnjuDszPKVGcLOXFx1HwAyheYoLsLUk8kgUCkBB1Z0sQ> 
Confirm your options are right for you 
Review and change your privacy and security options to make Google work   
better for you. 
Confirm<https://notifications.google.com/g/p/APdRdFxdj5YCPqoqGzXUhAkWe7PCqkyp7p3KOVG99H9vvyAYOW0BZh1lsZVsb9wzGRNgFyefg-a5C5Cd22PhT6iYnQxvvQaaoqcsnaS_EUH5TIfflEIAmotG9TFvFsnvKY0ieAWM_OJqZsW2mON6svKPUJrtxNIe2qCqKySZ5HBsUE0QRBUFd3bZteYwlaVMmqk5nuQlhqPBRoTeBbpOqAmNF9CpI8jNNrnwjdK-Q-Ymge-MCPzOkUuo2H3MhLHCPXaMNWF3yagSKTpktOep9Rw-SEpLoQReAlJn9voOnSUcQJe-59dqJDx1qzms> 
 
Replies to this email aren't monitored. If you have a question about your   
new account, the Help   
Center<https://notifications.google.com/g/p/APdRdFySnpq33dx3WIKP_Uqji0LAvGkX6pFL4WGLbqX6uXK7VJu1pfYaTKss8Yj5B85MNTML-2zxnPx4UKFVYx1wm4FzhuzjoElM6TsBpp2Ll82atX_vxbfgyoc3F9DNdEFwr9xtam-SR6Fv5VpaimydlLrmmI6RtUOW7nUfmNfl2rpqWocEt1rawIVGXXDy9ee1Xw0sbO9IJ4-rYb51-BvnYvEIew9tQF4Lpr6RpF13ftYdzBHbW6SL2xMfaw762ezxr-KyeiXVARzbwCQMOBqc7tCPcsI>   
likely has the answer you're looking for. 
 
 
Google LLC 1600 Amphitheatre Parkway, Mountain View, CA 94043 
 
This email was sent to you because you created a Google Account. 
 
 
`}</Text>
<Text>{`["https://notifications.google.com/g/p/APdRdFwgyeD2Ig8ZEIVz1e2l9QTOPqMd2OzB9zfFli8u-rARJgIOKiDToT0aZab3QV_5ppf6ZEYPqqA8dxrT2DWQ2_2eAihP_j33IzVU4HeeZ2zfu-gRDAFG50VAcoXRjDPhiWOIcnSbXDgW5yyswynXazhz83NDXRoemoFrVbrNpwF8_QRdXhiypGaNHFh25JJuzft2d3qrSzHKxTaWmULf9WJEn8SjU43m4d2h248cDXGythFbsGrw8MdrfkbJ1ojgCwSdIQ-xE2o_6VLExeJp_1A6ajKxRUvyO2h1OHynxWGwBi5kJWhOiuZ5guhjKLTQ3rY834Swj7rhacW9ia1P35jpgKljW0jaTp1NSUmNosHkiChfU9qnTArhK8x7wZOoA0JYPczrPqeP2782iJqaHCoMEuw2gaqGEdZb0XRMWfPh0Y_T5-1ij46NxV0wYlu3QLn65JZCUWEoIK73CKmfsHBaRLgKRRd4cTYL2qhgOBrdtI_BwEqveVXdLY3lQXAntEZn8_THZsiW0LAVcsR2MYwxWwemkJLY5ShuaKIlOwMDYMNxuSfGO7mOAPy8", "https://notifications.google.com/g/p/APdRdFwjttxARUhGfC0tURqJYGzO_xe_yyQhBsiS8qv7Zo-ijssQFqfcPKj04Zrn4Mik0Ct7eXslFoKA8IrNQ94jMCMAoTg7CGuxRi1rsx9AjG2r4skv62DnBfZYRLUMY5yUrxb47lB03e3ppa8kB1o_afAvrBVElR7XZZaClzHiGo8mzAJ_yuohewXJwYj9K6aAdtDGUzK--ADb07gvQhzUNvZEyNtNKKMvzrNwEfJfMl4n6zw-41LW-Nck0LKHzv-uM8cILGMVsDFLCMm6RdPBkp01-w9lmInxDeDxEQ8uOPSrFmzMWBqrD9GJlH6Ei7BTjL-NO7MgIb4BX8bgSxUg4Rq_WeY_7V-s6_f3vfFn2TnTQeXgBHVbDHPgWeqdlmfBK96LCfNoZ7KpdG9Iu_7lTznBXiucT9lMLVaGIsd5g_6_6MXXvu--_6Eft41HIDQfRD8fnGl81yyOZwHSgZ7_Dp3lRqWt5A_8qIOPxBejOOWGNuwuHzbDN_-h3GwkRaGYIkFwpHdFO8j2dfYiDxeYgep19JWZjKSa3Wt-B88ibdyRabayU-CjcSv1oamROg", "https://notifications.google.com/g/p/APdRdFyJivR-gBYMRsTTiyCsL_n6Iaz3ntNt_fycfiNvpvFAvIYCbskE7nv8gf2qoT4bAjmWEy7j5msOmAnEhrbvXd4OhQ31CdQcOLnoXN8AlAgbsu5bCupe-WRW3EVkBaFHePbExbcfSuxrkvPE9_MIkdZJOh-sY0Il34GKXh0iVzy3rVvT7nczoFHCd9GO06TGoDZ2c4YQ3pb2gMoKHKbInvvqPm0GYAg1xDVHUIPMvaYtwUi32BaO1PYQZN8VtAU-H18AAIk0bsNz3Td7YZz4Pu8ek5Nrgb1vJ8MlczpErIHH4Kmfj24je-kDdtDuOvE0I-Brw8-ma3qm4dpVMu6vLREtadtRHhtn2Q", "https://notifications.google.com/g/p/APdRdFweHsW4rIQeiA4qmrZ61liWOwXABmkkuxpKnMB2OnGtCe75r8fP1hKe9yfp-hdUdLwkEWKS9oVoiUMc8EPaqHLVVlJcQcEHd_ha5aGra7zla06dhw-JRGpKhXTpK6wD6aOa2zfECZL606UgVmZrS64yjc3paW754WdObXTe2HbyIGo3RueEc9rjuXXo8Ea7EtAJvJFod0lahWEFwF4FK4UFMUAJpKGLm6eTef3XZCNZ1z1yHNJSiY77IAv-Od_qxDkcHn_7Nvcc7e2Qi25Xi4GE6C7yZesjbh7vb3Gj6LZvTUZtwo8rg0eGadRyufwxtqqpaiT3FXTyXrDgdVYJNDKsTgmYbF8Razg", "https://notifications.google.com/g/p/APdRdFy_grULWqj0r7KicKvQmLN-oxB-tvnTTvwMQCcw2_PYH9nzzpnLiB9WQYoXi-VWXbOnmrAM7ymRHt7iX5qspSHXEbNdycNOeJMbRkg9AduXcbtDW_eTr5V6EBxcb6MIP0F6gZ9j_Dale6oufq5uCpRqBt07qSzxFu_pHP-_TRfTOgbAVQfCj_zNDyR8B7RLD3u04BDZaW0nZlqNtk6E5E8RMiif7wPpX7vR9eEx4n_tCAKphO1kf0rH1a3Kqg7s1iYWiADRSWh3wpURgCJs-H8SRy-e_SFbuF3DHiJoFwZQME6Oft3aTsbXqxKMaCBTdpx1tnkSjTI18H-uyiq7yoISHARyJC0-k5qBWv-Jy0PgbhghdB5fz9Jw0k1Ac9eHhHabZuFjqB4NsuIX2-MABxyV6n6RZ7LhTGVMZqMcZapiqiwrPY7PSZUGxUTsRCulPTBO-PvFi2_QR2Ha6GisIarIDpD9E9r8a9vvWOHFnI0oOs4GKF8w5dT1Yf_WJHEgapDas2Ks2Hm4fDDkqMoIrIjkhL4JbMHMQlXG2RlTVIkfNC4zYXCMcIcoHHNZojXIr7srZw0ygtGuXJAuod-fyJ3n5yi5-8KrqhvemJs_6byAhk5KMNOj5gg1OtoVeMKa_zG9Fpa8sG8", "https://notifications.google.com/g/p/APdRdFxX28ST_hbbTvnhyA3oQj7biSk2GAMJW_yeAIGQgZFNYD3cPSLJ1ffsomTwxRz7sDmVigct8rmhmwkLIGbL9TU8-FwA6aRjkTXjg4u0mVkEeu1ANnBySv4S0oftPy-bjd10qsSpWoYGbSiyNaUAd1J8LMmBK6q2eXGhxVokitEBEET-ApzNUsoGxge_ZWgHHFrnuoeogKMGVNZ-_cLR9O2Cwe9NAKlox5NlzboYQ2eljjkYtMLrpg0QdWQ62Hm1cZe8XGS0EC_8-UySHBIC1ks3FBEjfOkNNzQm07I-L9VVXWxONZG76DvFzNup0DpApaiDv1BprE_TsiXhV9WDQc2fDtbMjdR8m4fCePqgVFBjAhu8Um4TfzqlXJCh-btjy3nCU6ejYWLFmobDrANQXW5BCYfdSFWs7SkmE4qcXJ8YvXpqVWRhTNAQw4cGNnCGBTOmwsG9uhxc5FPAYXuALMn9W7sGl8GRxHyzUdAdnERGx88aG-wKuQD--2vyc97-0MpOKSGiNASVd7IEUcEUgTzZVYFKIhFXWym6h-acs_CxdCtuRqAr09pGaIJjh0-OMvKzqRwl2-5ozhTnDn88r1oA-zfEtYGZHBpF3u9VJW87k8QMUjxJYBw0sqLMPLEQwXRPlSWuXwFF", "https://notifications.google.com/g/p/APdRdFz_itmsd2WLHTg8K8W3eePq3eYaS01UJQm_Q9VT6EDFdIj665CUMq0AKpv9-mE4ZvlYVy6iaXbrX12qgUsHTuW39Z1iePDcAoXmxMZWt14b8yJIRCbkVPmvDdxnwjQ3i-YEPkG4fQxvqq8ya8g3BwfqJeinmItqcnWXZAOHfBIFN_WxgxPP0alY4z450L9HdSjYEMdriD38P1D5338Mc37l0OqIMAtKtkgBeLC1AWO995GVGrFGJ3oa4eTjccna6OA6-I4J8fVOtMrMq6Xe1IbU79sCJjkFXrGT_Xe1sA11QBuWQ0PSTXa-A7iJOnYnDrEhlxAVy8bTqT-JyQPDil0tMfx1vpuYqpn7xl7wRx2QfZOp_16Vs7GWTQ", "https://notifications.google.com/g/p/APdRdFwC8mXc5tBPUptckZzVjJq_97JIevAlxCHBUSXnWkrePa66dbGC4WdPIB4KxNDDxc-45FOTPLaNCAepf6oCFWXkqj3GRvZw_gjsAeINLdlWo8Psv3cE_23YKhWaXw3Rm_HW_CAogd_2Et-8aRHgcA7Qgl72HYTdXDq1EIpXF9gN2MnrA_tLnI-OflvpEWo_NwmWA5SzT4BbAJOAkxkiDgov86MsxnUKUG6pM6eKbBtZzEKpqjsE3_5tcPYXxLNVzOjqHdoG2VxOnjuDszPKVGcLOXFx1HwAyheYoLsLUk8kgUCkBB1Z0sQ", "https://notifications.google.com/g/p/APdRdFxdj5YCPqoqGzXUhAkWe7PCqkyp7p3KOVG99H9vvyAYOW0BZh1lsZVsb9wzGRNgFyefg-a5C5Cd22PhT6iYnQxvvQaaoqcsnaS_EUH5TIfflEIAmotG9TFvFsnvKY0ieAWM_OJqZsW2mON6svKPUJrtxNIe2qCqKySZ5HBsUE0QRBUFd3bZteYwlaVMmqk5nuQlhqPBRoTeBbpOqAmNF9CpI8jNNrnwjdK-Q-Ymge-MCPzOkUuo2H3MhLHCPXaMNWF3yagSKTpktOep9Rw-SEpLoQReAlJn9voOnSUcQJe-59dqJDx1qzms", "https://notifications.google.com/g/p/APdRdFySnpq33dx3WIKP_Uqji0LAvGkX6pFL4WGLbqX6uXK7VJu1pfYaTKss8Yj5B85MNTML-2zxnPx4UKFVYx1wm4FzhuzjoElM6TsBpp2Ll82atX_vxbfgyoc3F9DNdEFwr9xtam-SR6Fv5VpaimydlLrmmI6RtUOW7nUfmNfl2rpqWocEt1rawIVGXXDy9ee1Xw0sbO9IJ4-rYb51-BvnYvEIew9tQF4Lpr6RpF13ftYdzBHbW6SL2xMfaw762ezxr-KyeiXVARzbwCQMOBqc7tCPcsI"]`}</Text>
<NextHead><title>{`Pynecone App`}</title>
<meta content="A Pynecone app."
name="description"/>
<meta content="favicon.ico"
property="og:image"/></NextHead></VStack>
)
}