function Game(canvas, cfg) {
  
    // Properties
    this.canvas   = canvas;
    this.ctx      = canvas.getContext("2d");
    this.matrix   = undefined;
    this.round    = 0;
    
    // Merge of the default and delivered config.
    var defaults = {
        cellsX    : 100,
        cellsY    : 80,
        cellSize  : 10,
        rules     : "23/3",
        gridColor : "#fff",
        cellColor : "#0062cc"
    };
    this.cfg = $.extend({}, defaults, cfg);
    
    // Initialize the canvas and matrix.
    this.init();
}

Game.prototype = {
  
    init: function() {
        //canvas na dimensions
        this.canvas.width  = this.cfg.cellsX * this.cfg.cellSize;
        this.canvas.height = this.cfg.cellsY * this.cfg.cellSize;
        
        // matrix ne initialize karyu
        this.matrix = new Array(this.cfg.cellsX);
        for (var x = 0; x < this.matrix.length; x++) {
            this.matrix[x] = new Array(this.cfg.cellsY);
            for (var y = 0; y < this.matrix[x].length; y++) {
                this.matrix[x][y] = false;
            }
        }
        
        this.draw();
    },
    
    // aa main mathakhut
    draw: function() {
    var x, y;
        // canvas clear kari cell set
        this.canvas.width = this.canvas.width;
        this.ctx.strokeStyle = this.cfg.gridColor;
        this.ctx.fillStyle = this.cfg.cellColor;
        
        // grid draw karse
        for (x = 0.5; x < this.cfg.cellsX * this.cfg.cellSize; x += this.cfg.cellSize) {
          this.ctx.moveTo(x, 0);
          this.ctx.lineTo(x, this.cfg.cellsY * this.cfg.cellSize);
        }

        for (y = 0.5; y < this.cfg.cellsY * this.cfg.cellSize; y += this.cfg.cellSize) {
          this.ctx.moveTo(0, y);
          this.ctx.lineTo(this.cfg.cellsX * this.cfg.cellSize, y);
        }

        this.ctx.stroke();
        
        // matrix draw karse
        for (x = 0; x < this.matrix.length; x++) {
            for (y = 0; y < this.matrix[x].length; y++) {
                if (this.matrix[x][y]) {
                    this.ctx.fillRect(x * this.cfg.cellSize + 1,
                                      y * this.cfg.cellSize + 1,
                                      this.cfg.cellSize - 1,
                                      this.cfg.cellSize - 1);
                }
            }
        }
    },
    
    // game of life na rules and cell calculation
    step: function() {
        // initalize buffer
    var x, y;
        var buffer = new Array(this.matrix.length);
        for (x = 0; x < buffer.length; x++) {
            buffer[x] = new Array(this.matrix[x].length);
        }
        
        // one whole situation of cell
        for (x = 0; x < this.matrix.length; x++) {
            for (y = 0; y < this.matrix[x].length; y++) {
                // padosi count
                var neighbours = this.countNeighbours(x, y);
                
                // rules 
                if (this.matrix[x][y]) {
                    if (neighbours == 2 || neighbours == 3)
                        buffer[x][y] = true;
                    if (neighbours < 2 || neighbours > 3)
                        buffer[x][y] = false;
                } else {
                    if (neighbours == 3)
                        buffer[x][y] = true;
                }
            }
        }
        
        // flip matrix
        this.matrix = buffer;
        this.round++;
        this.draw();
    },
    countNeighbours: function(cx, cy) {
        var count = 0;
        
        for (var x = cx-1; x <= cx+1; x++) {
            for (var y = cy-1; y <= cy+1; y++) {
                if (x == cx && y == cy)
                    continue;
                if (x < 0 || x >= this.matrix.length || y < 0 || y >= this.matrix[x].length)
                    continue;
                if (this.matrix[x][y])
                    count++;
            }
        }
        
        return count;
    },
    
    //clear aakhi matrix
    clear: function() {
        for (var x = 0; x < this.matrix.length; x++) {
            for (var y = 0; y < this.matrix[x].length; y++) {
                this.matrix[x][y] = false;
            }
        }
        
        this.draw();
    },
    
    //randomize matrix
    randomize: function() {
        for (var x = 0; x < this.matrix.length; x++) {
            for (var y = 0; y < this.matrix[x].length; y++) {
                this.matrix[x][y] = Math.random() < 0.3;
            }
        }
        
        this.draw();
    },
    
    // toggle state of cell blue ke white
    toggleCell: function(cx, cy) {
        if (cx >= 0 && cx < this.matrix.length && cy >= 0 && cy < this.matrix[0].length) {
            this.matrix[cx][cy] = !this.matrix[cx][cy];
            this.draw();
        }
    }
};


// animation loop
var timer;

// Initialize game
var game = new Game(document.getElementById("game"));

// run or stop
$("#run").click(function() {
  if (timer === undefined) {
    timer = setInterval(run, 40);
    $(this).text("Stop");
  } else {
    clearInterval(timer);
    timer = undefined;
    $(this).text("Start");
  }
});

// one step
$("#step").click(function() {
  if (timer === undefined) {
    game.step();
    $("#round span").text(game.round);
  }
});

// clear
$("#clear").click(function() {
  game.clear();
  game.round = 0;
  $("#round span").text(game.round);
});

// Rand lul
$("#rand").click(function() {
  game.randomize();
  game.round = 0;
  $("#round span").text(game.round);
});

// register onclick on the canvas
game.canvas.addEventListener("click", gameOnClick, false);

function gameOnClick(e) {
    var x;
    var y;
    
    // determen click position
    if (e.pageX !== undefined && e.pageY !== undefined) {
        x = e.pageX;
        y = e.pageY;
    } else {
        x = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        y = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }
    
    // set cnavas compablitity
    x -= game.canvas.offsetLeft;
    y -= game.canvas.offsetTop;
    
    // calculate clicked cell
    x = Math.floor(x/game.cfg.cellSize);
    y = Math.floor(y/game.cfg.cellSize);
    
    game.toggleCell(x, y);
}

//run counter 
function run() {
    game.step();
    $("#round span").text(game.round);
}

game.randomize();