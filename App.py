import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird", page_icon="🐤")

st.title("🐤 FLAPPY BIRD")
st.write("Bấm hoặc chạm màn hình để chim bay lên, né ống và ghi điểm!")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  margin: 0;
  background: #70c5ce;
  font-family: Arial, sans-serif;
  text-align: center;
  overflow: hidden;
}
canvas {
  display: block;
  margin: auto;
  width: 100%;
  max-width: 420px;
  background: #70c5ce;
  border: 3px solid #ffffff;
  border-radius: 10px;
  touch-action: manipulation;
}
button {
  margin-top: 10px;
  padding: 12px 28px;
  font-size: 18px;
  font-weight: bold;
  background: #ffcf33;
  border: 0;
  border-radius: 12px;
  cursor: pointer;
}
p { color: #17324d; font-weight: bold; }
</style>
</head>
<body>
<canvas id="game" width="360" height="500"></canvas>
<p>Chạm màn hình hoặc nhấn SPACE để bay!</p>
<button id="start">▶ Bắt đầu / Chơi lại</button>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const startBtn = document.getElementById("start");

let bird, pipes, score, frame, playing, started;

function reset() {
  bird = {x: 75, y: 220, v: 0, r: 13};
  pipes = [];
  score = 0;
  frame = 0;
  playing = true;
  started = true;
  bird.v = -5;
}

function flap() {
  if (!started || !playing) return;
  bird.v = -5.5;
}

function action() {
  if (!started || !playing) {
    reset();
    return;
  }
  flap();
}

startBtn.addEventListener("click", reset);
canvas.addEventListener("pointerdown", action);
document.addEventListener("keydown", e => {
  if (e.code === "Space" || e.code === "ArrowUp") {
    e.preventDefault();
    action();
  }
});

function drawBird() {
  ctx.save();
  ctx.translate(bird.x, bird.y);
  ctx.rotate(Math.min(Math.PI/4, bird.v * 0.07));
  ctx.fillStyle = "#ffd83d";
  ctx.beginPath();
  ctx.arc(0, 0, bird.r, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle = "#a87500";
  ctx.lineWidth = 2;
  ctx.stroke();
  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.arc(5, -4, 5, 0, Math.PI*2);
  ctx.fill();
  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.arc(7, -4, 2, 0, Math.PI*2);
  ctx.fill();
  ctx.fillStyle = "#ff7043";
  ctx.beginPath();
  ctx.moveTo(10, 1);
  ctx.lineTo(22, 5);
  ctx.lineTo(10, 8);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawPipe(p) {
  const bottomY = p.top + p.gap;
  ctx.fillStyle = "#27b84a";
  ctx.fillRect(p.x, 0, 48, p.top);
  ctx.fillRect(p.x - 4, p.top - 18, 56, 18);
  ctx.fillRect(p.x, bottomY, 48, 500 - bottomY);
  ctx.fillRect(p.x - 4, bottomY, 56, 18);
  ctx.strokeStyle = "#167c32";
  ctx.lineWidth = 2;
  ctx.strokeRect(p.x, 0, 48, p.top);
  ctx.strokeRect(p.x, bottomY, 48, 500 - bottomY);
}

function textCenter(text, y, size, color) {
  ctx.fillStyle = color;
  ctx.font = "bold " + size + "px Arial";
  ctx.textAlign = "center";
  ctx.fillText(text, 180, y);
}

function update() {
  frame++;

  ctx.clearRect(0, 0, 360, 500);

  // Clouds
  ctx.fillStyle = "rgba(255,255,255,0.75)";
  for (const c of [[55,75],[250,110],[160,40]]) {
    ctx.beginPath();
    ctx.arc(c[0], c[1], 18, 0, Math.PI*2);
    ctx.arc(c[0]+18, c[1]-7, 22, 0, Math.PI*2);
    ctx.arc(c[0]+38, c[1], 16, 0, Math.PI*2);
    ctx.fill();
  }

  ctx.fillStyle = "#d9f3a5";
  ctx.fillRect(0, 465, 360, 35);
  ctx.fillStyle = "#b9e36b";
  ctx.fillRect(0, 465, 360, 7);

  if (playing && started) {
    bird.v += 0.28;
    bird.y += bird.v;

    if (frame % 95 === 0) {
      let top = 70 + Math.random()*220;
      pipes.push({x: 365, top: top, gap: 155, passed: false});
    }

    for (const p of pipes) {
      p.x -= 2.3;
      drawPipe(p);

      if (!p.passed && p.x + 48 < bird.x) {
        score++;
        p.passed = true;
      }

      if (
        bird.x + bird.r > p.x &&
        bird.x - bird.r < p.x + 48 &&
        (bird.y - bird.r < p.top ||
         bird.y + bird.r > p.top + p.gap)
      ) {
        playing = false;
      }
    }

    pipes = pipes.filter(p => p.x > -60);

    if (bird.y + bird.r >= 465 || bird.y - bird.r <= 0) {
      playing = false;
    }
  } else {
    for (const p of pipes) {
      drawPipe(p);
    }
  }

  drawBird();

  ctx.textAlign = "center";
  ctx.font = "bold 30px Arial";
  ctx.lineWidth = 4;
  ctx.strokeStyle = "#ffffff";
  ctx.strokeText(score, 180, 55);
  ctx.fillStyle = "#18364d";
  ctx.fillText(score, 180, 55);

  if (!started) {
    textCenter("FLAPPY BIRD", 210, 30, "#ffffff");
    textCenter("Bam BAT DAU de choi!", 250, 17, "#17324d");
  }

  if (started && !playing) {
    ctx.fillStyle = "rgba(0,0,0,0.55)";
    ctx.fillRect(25, 165, 310, 130);
    textCenter("GAME OVER!", 210, 30, "#ffdf4d");
    textCenter("Diem cua ban: " + score, 245, 21, "#ffffff");
    textCenter("Nhan Choi lai ben duoi", 273, 15, "#ffffff");
  }

  requestAnimationFrame(update);
}

started = false;
playing = false;
bird = {x:75, y:220, v:0, r:13}
