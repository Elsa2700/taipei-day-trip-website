

// ================================
var statusTable = {
    '0': '欄位已填好，並且沒有問題',
    '1': '欄位還沒有填寫',
    '2': '欄位有錯誤，此時在 CardView 裡面會用顯示 errorColor',
    '3': '使用者正在輸入中',
}
var defaultCardViewStyle = {
    color: 'rgb(0,0,0)',
    fontSize: '15px',
    lineHeight: '24px',
    fontWeight: '300',
    errorColor: 'red',
    placeholderColor: ''
}
var config = { 
    isUsedCcv: false 
}
TPDirect.card.setup('#tappay-iframe', defaultCardViewStyle, config)
TPDirect.card.onUpdate(function (update) {

    var submitButton = document.querySelector('#submit')
    var cardViewContainer = document.querySelector('#tappay-iframe')

    if (update.canGetPrime) {
        submitButton.removeAttribute('disabled')
    } else {
        submitButton.setAttribute('disabled', true)
    }

    var message = document.querySelector('#message')

    message.innerHTML = `
        canGetPrime: ${update.canGetPrime} \n
        cardNumberStatus: ${statusTable[update.status.number]} \n
        cardExpiryStatus: ${statusTable[update.status.expiry]} \n
        cvcStatus: ${statusTable[update.status.cvc]}
    `.replace(/    /g, '')

    if (update.hasError) {
        message.classList.add('error')
        message.classList.remove('info')
    } else {
        message.classList.remove('error')
        message.classList.add('info')
    }
})
document.querySelector('#submit').addEventListener('click', function(event) {
    TPDirect.card.getPrime(function(result) {
        document.querySelector('#result').innerHTML  = JSON.stringify(result, null, 4)

        var command = `
        Use following command to send to server \n\n
        curl -X POST https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime \\
        -H 'content-type: application/json' \\
        -H 'x-api-key: partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM' \\
        -d '{
            "partner_key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM",
            "prime": "${result.card.prime}",
            "amount": "1",
            "merchant_id": "GlobalTesting_CTBC",
            "details": "Some item",
            "cardholder": {
                "phone_number": "+886923456789",
                "name": "王小明",
                "email": "LittleMing@Wang.com",
                "zip_code": "100",
                "address": "台北市天龍區芝麻街1號1樓",
                "national_id": "A123456789"
            }
        }'`.replace(/                /g, '')

        document.querySelector('#curl').innerHTML = command
    })
})