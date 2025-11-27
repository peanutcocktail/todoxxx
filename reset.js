module.exports = {
  run: [
    {
      when: "{{exists('app/venv')}}",
      method: "fs.rm",
      params: {
        path: "app/venv"
      }
    },
    {
      when: "{{exists('app/data/todos.db')}}",
      method: "fs.rm",
      params: {
        path: "app/data/todos.db"
      }
    },
    {
      when: "{{exists('app/__pycache__')}}",
      method: "fs.rm",
      params: {
        path: "app/__pycache__"
      }
    }
  ]
}
