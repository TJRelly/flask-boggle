class Boggle {
  constructor(time = 60) {
    this.guesses = [];
    this.time = time;
    this.score = 0;
    this.interval = setInterval(this.startTimer.bind(this), 1000);
    $("form").on("submit", this.handleSubmit.bind(this));
  }

  play() {
    this.interval;
  }

  handleSubmit(e) {
    e.preventDefault();
    const guess = $(".guess_field");
    this.makeGuess(guess.val());
    guess.val("");
  }

  startTimer() {
    $(".timer").text(`Time Left: ${this.time}`);
    this.time -= 1;
    if (this.time < 0) {
      clearInterval(this.interval);
      this.showMsg(`Game Over. You scored ${this.score} points!`);
      $("form").off().on("click", this.showGameOver.bind(this));
      this.getStatisics(this.score);
    }
  }

  async makeGuess(guess) {
    //Handling duplicate guesses
    if (!this.guesses.includes(guess)) {
      const res = await axios.post("/guess", { guess: guess });
      const result = res.data.result;
      if (result === "ok") {
        this.showMsg(`Congradulations! You found: "${guess}".`);
        this.score += guess.length;
        this.showScore(this.score);
        this.guesses.push(guess);
      } else if (result === "not-on-board") {
        this.showMsg(`Sorry, "${guess}" is not on the board.`);
      } else this.showMsg(`Sorry, "${guess}" is not a word.`);
    } else this.showMsg(`You've already guessed "${guess}"!`);
  }

  async getStatisics(score) {
    const res = await axios.post("/score", { score: score });
    const highScore = res.data.high_score;
    const gamesPlayed = res.data.games_played;
    $(".high_score").text(`High Score: ${highScore}`);
    $(".games_played").text(`Games Played: ${gamesPlayed}`);
  }

  showMsg(msg) {
    $(".msg").text(msg);
  }

  showScore(score) {
    $(".score").text(`Current Score: ${score}`);
  }

  showGameOver(e) {
    e.preventDefault();
    this.showMsg(`Game Over. You scored ${this.score} points!`);
  }
}

const boggle = new Boggle(60);
boggle.play();
