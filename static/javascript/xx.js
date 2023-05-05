

function leftIndexOf(array, startIndex, element) {
    let index = startIndex;
    while (index > -1 && array[index] !== element)
        index--;
    return index;
}


const ar = ['a', 'b', 'c', 'd', 'e', 'f'];

const p = leftIndexOf(ar, 4, 'a');
console.log(p);
console.log(ar[p]);