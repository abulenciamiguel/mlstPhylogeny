# Constructing Maximum Likelihood tree from MLST genes

1.  Extract genes from reference genome using base positions then reverse complement

      |  Gene  |  Start    |  End      |
      |  ----  |  -------  |  -------  |
      |  arcC  |  1454446  |  1454882  |
      |  nrdE  |  1225274  |  1225721  |
      |  proS  |  187680   |  188114   |
      |  spi   |  1702578  |  1703036  |
      |  tdk   |  945014   |  945383   |
      |  tpi   |  662015   |  662438   |
      |  yqiL  |  533219   |  533614   |

    ```
    samtools faidx \
    -i NZ_CP065061_1.fasta \
    NZ_CP065061.1:533219-533614 > mlst_genes/reverse_alleles/NZ_CP065061.1.yqiL.fasta
    ```

2.  Concatenate contigs into pseudogenomes
    ```
    while read line
    do
    echo ">${line}" > consensus_new/${line}.fasta
    done < consensus/list.txt
    ```
    ```
    while read line
    do
    grep -v '>' consensus/${line}.fasta >> consensus_new/${line}.fasta
    done < consensus/list.txt
    ```
3.  Extract the alleles from the consensus sequence
    ```
    for allele in arcC nrdE proS spi tdk tpi yqiL
    do
    	while read line
    	do
    
    	mkdir -p extract_allelles/${line}/
    
    	blastn -query consensus_new/${line}.fasta \
    	-subject reverse_alleles/NZ_CP065061.1.${allele}.fasta \
    	-outfmt 6 \
    	-out res.tsv
    
    
    	python extractRegion.py \
    	consensus_new/${line}.fasta \
    	extract_allelles/${line}/${line}.${allele}.fasta \
    	res.tsv
    
    
    	rm res.tsv stripped.fasta
    	done < consensus/list.txt
    done
    ```
4.  Concatenate the MLST genes of a sample into a single fasta file
    ```
    while read line
    do
    
    cat extract_allelles/${line}/${line}*fasta > comb.fasta
    
    echo ">"${line} > extract_allelles/${line}/mlst.${line}.fasta
    
    grep -v ">" comb.fasta >> extract_allelles/${line}/mlst.${line}.fasta
    
    rm comb.fasta
    done < consensus/list.txt
    ```
5.  Concatenate the mlst files into a single multi-fasta file
    ```
    mkdir -p tree
    
    cat extract_allelles/*/mlst*fasta > tree/mlst.fasta
    ```
6.  Do multiple sequence alignment of the multi-fasta file using MAFFT's G-INS-i
    ```
    ginsi \
    --maxiterate 1000 \
    tree/mlst.fasta > tree/mlst.msa.fasta
    ```
7.  Reconstruct the Maximum likelihood tree
    ```
    iqtree -T 32 \
    -s tree/mlst.msa.fasta \
    -m TIM2+I+G \
    -alrt 1000 \
    -bb 1000 \
    -pre tree/mlst
    ```
