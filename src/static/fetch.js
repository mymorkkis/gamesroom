function movePiece(event) {
  if (move['from'] === null) {
    move['from'] = event.id
  }
  else {
    makeMove(event.id)
  }
}

function placePiece(event) {
  makeMove(event.id)
}

async function makeMove(event_id) {
  move['to'] = event_id
  const moveRoute = `move?from=${move['from']}&to=${move['to']}`
  const warningH1 = document.getElementById('game-error')

  try {
    const fetchResult = fetch(moveRoute)
    const response = await fetchResult
    const jsonData = await response.json()

    if (jsonData.err) {
      warningH1.innerText = jsonData.err
    }
    else {
      warningH1.innerText = ''
      updateBoard(jsonData.board)
    }
  } catch(e){
    throw Error(e);
  }

  reset_move()
}

function updateBoard(board) {
  for (const row of board) {
    for (const [square_id, image] of row) {
      const square = document.getElementById(square_id)
      square.innerText = image
    }
  }
}

function reset_move() {
  move['from'] = null
  move['to'] = null
}

let move = {
  'from': null,
  'to': null
}
