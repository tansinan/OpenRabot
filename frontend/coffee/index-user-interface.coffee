@userInterface =
  left: -90
  right: 90
  move: (step, callback) ->
    stepX = step * Math.sin(gameScene.rabbit.angle / 180.0 * Math.PI)
    stepY = step * Math.cos(gameScene.rabbit.angle / 180.0 * Math.PI)
    gameScene.moveRabbit stepX, -stepY, Math.abs(5 * step), callback
  turn: (angle, callback) ->
    gameScene.rotateRabbit angle, Math.abs(5 * angle), callback

@enableUserInterface = (gameScene) ->
  @gameScene = gameScene
  for key, value of @userInterface
    this[key] = value
  return undefined

@executeUserCode = (jsCode) ->
  eval jsCode

@disableUerInterface = ->
  for key, value of @userInterface
    this[key] = undefined
  @gameScene = undefined
  return undefined

@userCodeFinished = ->
  if @gameScene.isWin()
    alert "You win!"
  else
    alert "You lose"
  disableUerInterface()
