
var entrada1 = document.getElementById('inputValid1');
var contenedor1 = document.querySelector('.form-group1');

var entrada2 = document.getElementById('inputValid2');
var contenedor2 = document.querySelector('.form-group2');

var entrada3 = document.getElementById('inputValid3');
var contenedor3 = document.querySelector('.form-group3');

var entrada4 = document.getElementById('inputValid4');
var contenedor4 = document.querySelector('.form-group4');

entrada1.addEventListener('keyup', function (e) {

  contenedor1.setAttribute('class', 'form-group has-success')
  entrada1.setAttribute('class', 'form-control is-valid')

  if (entrada1.value == '') {

    contenedor1.setAttribute('class', 'form-group has-danger')
    entrada1.setAttribute('class', 'form-control is-invalid')

  } else if (entrada1.value.includes('@')) {
    contenedor1.setAttribute('class', 'form-group has-danger')
    entrada1.setAttribute('class', 'form-control is-invalid')

  } else if (entrada1.value.includes(' ')) {
    contenedor1.setAttribute('class', 'form-group has-danger')
    entrada1.setAttribute('class', 'form-control is-invalid')

  }
})


entrada2.addEventListener('keyup', function (e) {

  contenedor2.setAttribute('class', 'form-group has-success')
  entrada2.setAttribute('class', 'form-control is-valid')


  if (entrada2.value == '') {
    contenedor2.setAttribute('class', 'form-group has-danger')
    entrada2.setAttribute('class', 'form-control is-invalid')

  } else if (!entrada2.value.includes('@')) {
    contenedor2.setAttribute('class', 'form-group has-danger')
    entrada2.setAttribute('class', 'form-control is-invalid')

  } else if (entrada2.value.includes(' ')) {
    contenedor2.setAttribute('class', 'form-group has-danger')
    entrada2.setAttribute('class', 'form-control is-invalid')

  }
})

entrada3.addEventListener('keyup', function (e) {

  contenedor3.setAttribute('class', 'form-group has-success')
  entrada3.setAttribute('class', 'form-control is-valid')


  if (entrada3.value == '') {

    contenedor3.setAttribute('class', 'form-group has-danger')
    entrada3.setAttribute('class', 'form-control is-invalid')

  } else if (entrada3.value.includes(' ')) {
    contenedor3.setAttribute('class', 'form-group has-danger')
    entrada3.setAttribute('class', 'form-control is-invalid')

  }
})

entrada4.addEventListener('keyup', function (e) {

  contenedor4.setAttribute('class', 'form-group has-success')
  entrada4.setAttribute('class', 'form-control is-valid')


  if (entrada4.value == '') {

    contenedor4.setAttribute('class', 'form-group has-danger')
    entrada4.setAttribute('class', 'form-control is-invalid')

  } else if (entrada4.value.includes(' ')) {
    contenedor4.setAttribute('class', 'form-group has-danger')
    entrada4.setAttribute('class', 'form-control is-invalid')

  }
})