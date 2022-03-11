#include <assert.h>
#include <stdbool.h>
#define SIZE 5

int intArray[SIZE] = {8, 12, 2, 5, 4};

void swap(int index1, int index2) {
  int temp = intArray[index1];
  intArray[index1] = intArray[index2];
  intArray[index2] = temp;
}

int partition(int left, int right, int pivot) {
  int leftPointer = left -1;
  int rightPointer = right;

  while(1) {
    while(intArray[++leftPointer] < pivot) {
      //do nothing
    }
  
    while(rightPointer > 0 && intArray[--rightPointer] > pivot) {
      //do nothing
    }

    if(leftPointer >= rightPointer) {
      break;
    } else {
      swap(leftPointer,rightPointer);
    }
  }

  swap(leftPointer,right);
  return leftPointer;
}

void quickSort(int left, int right) {
  if(right-left <= 0) {
    return;   
  } else {
    int pivot = intArray[right];
    int partitionPoint = partition(left, right, pivot);
    quickSort(left,partitionPoint-1);
    quickSort(partitionPoint+1,right);
  }        
}

bool is_sorted() {
  for (int i = 0; i < SIZE - 1; i++) {
    if (intArray[i] > intArray[i + 1]) {
      return false;
    }
  }

  return true;
}

int main() {
  klee_make_symbolic(&intArray, sizeof(intArray), "intArray");
  // quickSort(0, SIZE-1);
  assert(is_sorted());
  return 0;
}