import {useState} from 'react';

function Square({value, onSquareClick, isChosen}){
  const highlight = {
    backgroundColor: isChosen ? 'yellow' : 'transparent',
  };
  return(
    <button className="square" style={highlight} onClick={onSquareClick}>{value}</button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [playerXCount, setPlayerXCount] = useState(0);
  const [playerOCount, setPlayerOCount] = useState(0);
  const [xThirdMove, setXThirdMove] = useState(false);
  const [oThirdMove, setOThirdMove] = useState(false);
  const [source, setSource] = useState(null);
  const [centerX, setCenterX] = useState(false);
  const [centerO, setCenterO] = useState(false);
  const [chosenSquare, setChosenSquare] = useState(null);

  
  function validMove(source, target)
  {
    const valid =
    {
      0: [1, 3, 4],
      1: [0, 2, 3, 4, 5],
      2: [1, 4, 5],
      3: [0, 1, 4, 6, 7],
      4: [0, 1, 2, 3, 5, 6, 7, 8],
      5: [1, 2, 4, 7, 8],
      6: [3, 4, 7],
      7: [3, 4, 5, 6, 8],
      8: [4, 5, 7],
    }

    const centerPairings =
    {
      0: 8,
      1: 7,
      2: 6,
      3: 5,
      5: 3,
      6: 2,
      7: 1,
      8: 0,
    }
    if(centerX && xIsNext)
    {
      setCenterX(false);
      if(centerPairings[target] && squares[centerPairings[target]] == "X")
      {
        return true;
      }
      if(source != 4)
      {
        setSource(null);
        return false;
      }
    }
    if(centerO && !xIsNext)
    {
      setCenterO(false);
      if(centerPairings[target] && squares[centerPairings[target]] == "O")
      {
        return true;
      }
      if(source != 4)
      {
        setSource(null);
        return false;
      }
    }
    return (valid[source] && valid[source].includes(target));
  }
  function moveSquares(updateSquares, source, target)
  {
    let temp = updateSquares[source];
    updateSquares[source] = null;
    updateSquares[target] = temp;
    return updateSquares;
  }
  
  function chorusLapelli(i)
  {
    if(source == null){
      if(squares[i] == null){
        return;
      }
      setSource(i);
      return;
    }
    if(squares[source] == "X" && !xIsNext) //x playing during o's turn
    {
      setSource(null); 
      return;
    }
    if(squares[source] == "O" && xIsNext) //o playing during x's turn
    {
      setSource(null); 
      return;
    }
    if(squares[i] == null && validMove(source, i)){
      const updateSquares = moveSquares(squares.slice(), source, i)
      setSquares(updateSquares);
      setXIsNext(!xIsNext);
      setSource(null);
    }else{
      setSource(null);
    }
    return;
  }

  function handleClick(i){
    setChosenSquare(i);
    if(calculateWinner(squares))
    {
      return;
    }
    if(xThirdMove || oThirdMove){
      if(squares[4] == "X"){
        setCenterX(true);
      }
      if(squares[4] == "O"){
        setCenterO(true);
      }
      chorusLapelli(i);
      return;
    }
    if(squares[i]){
      return;
    }
    const nextSquares = squares.slice();
    if(xIsNext){
      nextSquares[i] = "X";
    }else{
      nextSquares[i] = "O";
    }
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
    
    if(xIsNext){
      setPlayerXCount(playerXCount+1);
    }else{
      setPlayerOCount(playerOCount+1);
    }
    if(playerXCount >= 3){
      setXThirdMove(true)
    }
    if(playerOCount >= 3){
      setOThirdMove(true)
    }
  }

 
  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O");
  }

  function resetBoard()
  {
    setXIsNext(true);
    setSquares(Array(9).fill(null));
    setPlayerXCount(0);
    setPlayerOCount(0);
    setXThirdMove(false);
    setOThirdMove(false);
    setSource(null);
    setChosenSquare(null);
  }

  return(
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} isChosen={chosenSquare === 0}/>
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} isChosen={chosenSquare === 1}/>
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} isChosen={chosenSquare === 2}/>
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} isChosen={chosenSquare === 3}/>
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} isChosen={chosenSquare === 4}/>
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} isChosen={chosenSquare === 5}/>
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} isChosen={chosenSquare === 6}/>
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} isChosen={chosenSquare === 7}/>
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} isChosen={chosenSquare === 8}/>
      </div>
      <div>
        <button onClick={resetBoard}>Reset Button</button>
      </div>
    </>
  );
}

function calculateWinner(squares) {
  if (!squares || squares.length !== 9) {
    return null;
  }
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

