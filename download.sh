#!/bin/zsh
for i in {1..13}
do
    wget http://www.quizbowlpackets.com/130/$i.pdf
    wget http://www.quizbowlpackets.com/533/R$i.pdf
done
