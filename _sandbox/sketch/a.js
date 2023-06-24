const r = 3;
let cell_dia, cell_rad, cell_size, grid_size, cells;

function init_grid_cells(w, h) {
  grid_size = Math.min(w, h);
  cell_dia = r * 2 + 1;
  cell_size = grid_size / cell_dia;

  const ranges = [...Array(cell_dia)].map((_, i) => i);

  cells = [...ranges].map((y) =>
    [...ranges].map((x) =>
      rect(x * cell_size, y * cell_size, cell_size, cell_size)
    )
  );

  console.log(cells);
}

function setup() {
  const size_width = 400;
  const size_height = 400;
  createCanvas(size_width, size_height);
  background(220);
  init_grid_cells(size_width, size_height);
}
