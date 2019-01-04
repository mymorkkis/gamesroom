function movePiece(event) {
  if (move['fromId'] === null) {
    const moveFromSquare = document.getElementById(event.id)
    moveFromSquare.classList.add('move-from-square')
    move['fromId'] = event.id

  } else {
    const moveFromSquare = document.getElementById(move['fromId'])
    moveFromSquare.classList.remove('move-from-square')

    tryMove(event.id)
  }
}

function placePiece(event) {
  tryMove(event.id)
}

async function tryMove(event_id) {
  move['toId'] = event_id
  const moveRoute = `move?from=${move['fromId']}&to=${move['toId']}`

  try {
    const fetchResult = fetch(moveRoute)
    const response = await fetchResult
    const jsonData = await response.json()

    makeMove(jsonData)

  } catch(e) {
    throw Error(e);
  }
}

function makeMove(gameData) {
  const gameError = document.getElementById('game-error')
  const gameWinner = document.getElementById('game-winner')
  const currentPlayer = document.getElementById('current-player')
  gameError.innerText = ''

  if (gameData.err) {
    gameError.innerText = gameData.err
  } else if (gameData.winner) {
    gameWinner.innerText = `${gameData.winner} wins!!! Refresh to play again.`
    updateBoard(gameData.board, gameEnd=true)
  } else {
    currentPlayer.innerText = gameData.next_player
    updateBoard(gameData.board)
  }

  reset_move()
}

function updateBoard(board, gameEnd=false) {
  for (const row of board) {
    for (const [square_id, image] of row) {
      const square = document.getElementById(square_id)
      square.innerText = image
      if (gameEnd) {
        square.onclick = null
      }
    }
  }
}

function reset_move() {
  move['fromId'] = null
  move['toId'] = null
}

let move = {
  'fromId': null,
  'toId': null
}
