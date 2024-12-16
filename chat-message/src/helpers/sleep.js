export const sleep = ( second = 1 ) => {
  return new Promise ( res => {
    setTimeout( res, second * 1000 );
  })
}
