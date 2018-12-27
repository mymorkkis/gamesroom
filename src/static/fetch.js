async function makeMove(event) {
  if (move['from'] === null) {
    move['from'] = event.id
  }
  else {
    move['to'] = event.id
    const moveRoute = `move?from=${move['from']}&to=${move['to']}`
    const warningH1 = document.getElementById('warn')

    try {
      const fetchResult = fetch(moveRoute)
      const response = await fetchResult
      const jsonData = await response.json()

      if (jsonData['err']) {
        warningH1.innerText = jsonData['err']
      }
      else {
        warningH1.innerText = ''
        updateBoard(jsonData)
      }
    } catch(e){
      throw Error(e);
    }

    reset_move()
  }
}

function updateBoard(jsonData) {
  const from_square = document.getElementById(move['from'])
  const to_square = document.getElementById(move['to'])

  from_square.innerText = jsonData['from_image']
  to_square.innerText = jsonData['to_image']
}

function reset_move() {
  move['from'] = null
  move['to'] = null
}

let move = {
  'from': null,
  'to': null
}
