var canvas, ctx;
var trainer, bg;
var sprite, spriteX, spriteY, spriteDX, spriteDY;
var pokeball, ballThrown, ballX, ballY, ballSize, ballsLeft, ballDX, ballDY;
var mouseX, mouseY;
var MAX_WIDTH = 800;
var MAX_HEIGHT = 480;

function setup() {
    canvas = document.getElementById("encounterCanvas");
    canvas.addEventListener('click', throwPokeball);
    //console.log(canvas);
    ctx = canvas.getContext("2d");
    //console.log(ctx);
    bg = document.getElementById("encounterBackground");
    trainer = document.getElementById("trainer");

    sprite = document.getElementById("sprite");
    spriteX = 400;
    spriteY = 110;
    spriteDX = 1;
    spriteDY = 1;

    pokeball = document.getElementById("pokeball");
    ballThrown = false;
    ballX = 220;
    ballY = 300;
    ballSize = 50;
    ballsLeft = 3;
}

function spriteInBoundsX() {
    var inBounds = true;
    inBounds = inBounds && spriteX > 350;
    inBounds = inBounds && spriteX < 550;
    return inBounds;
}

function spriteInBoundsY() {
    var inBounds = true;
    inBounds = inBounds && spriteY > 100;
    inBounds = inBounds && spriteY < 200;
    return inBounds;
}

function throwPokeball(e) {
    if (!ballThrown) {
        ballThrown = true;
        mouseX = e.pageX - canvas.offsetLeft;
        mouseY = e.pageY - canvas.offsetTop;
        ballDX = (mouseX - ballX) / 100;
        ballDY = (mouseY - ballY) / 100;
        ballsLeft--;
    }
}

function dist(x1, y1, x2, y2) {
    return Math.sqrt((x2-x1)**2 + (y2-y1)**2);
}

function update() {
    if (!spriteInBoundsX()) {
        console.log("switch DX");
        spriteDX *= -1;
    }
    if (!spriteInBoundsY()) {
        console.log("switch DY");
        spriteDY *= -1;
    }
    if (ballThrown) {
        //move ball linearly towards mouse coords
        ballX += ballDX;
        ballY += ballDY;
        if (dist(ballX, ballY, mouseX, mouseY) < 10) {
            //check if capture
            ballThrown = false;
            //console.log(dist(ballX + 25, ballY + 25, spriteX + 100, spriteY + 100));
            if (dist(ballX, ballY, spriteX + 100, spriteY + 100) < 50) {
                console.log("caught pokemon");
                alert("You caught the pokemon!");
                window.location = "/caught";
            } else {
                ballX = 220;
                ballY = 300;
                //console.log('checking ballsLeft');
                if (ballsLeft == 0) {
                    alert("The pokemon ran away!");
                    window.location = "/map";
                }
            }
        }
    } else {
        spriteX += spriteDX;
        spriteY += spriteDY;
    }
}

function draw() {
    ctx.drawImage(bg, 0, 0);
    ctx.drawImage(trainer, -50, 100);
    ctx.drawImage(sprite, spriteX, spriteY, 200, 200);
    //draw sprite hitbox
    ctx.beginPath();
    ctx.arc(spriteX + 100, spriteY + 100, 50, 0, 2*Math.PI);
    ctx.stroke();
    if (ballThrown) {
        //console.log(pokeball + " " + ballX + " " + ballY + " " + ballSize);
        ctx.drawImage(pokeball, ballX - 25, ballY - 25, ballSize, ballSize);
        //draw pokeball hitbox
        ctx.beginPath();
        ctx.arc(ballX, ballY, 5, 0, 2*Math.PI);
        ctx.stroke();
    }
    for (var i = 0; i < ballsLeft; i++) {
        ctx.drawImage(pokeball, 300 + 60 * i, 400, ballSize, ballSize);
    }
}

setup();

setInterval(function() {
    update();
    draw();
}, 10);
