# hiast2-参数
Website: http://daehwankimlab.github.io/hisat2/
```
HISAT2 version 2.1.0 by Daehwan Kim (infphilo@gmail.com, www.ccb.jhu.edu/people/infphilo)
Usage: 
  hisat2 [options]* -x <ht2-idx> {-1 <m1> -2 <m2> | -U <r>} [-S <sam>]

  <ht2-idx>  Index filename prefix (minus trailing .X.ht2).
             索引文件的前缀
  <m1>       Files with #1 mates, paired with files in <m2>.
             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
             Paired-end测序的第一个文件，可以是压缩格式的（`.gz`或者`.bz2`）
  <m2>       Files with #2 mates, paired with files in <m1>.
             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
             Paired-end测序的第二个文件
  <r>        Files with unpaired reads.
             Could be gzip'ed (extension: .gz) or bzip2'ed (extension: .bz2).
             single-end测序的文件
  <sam>      File for SAM output (default: stdout)
             输出比对的结果（`.sam`）

  <m1>, <m2>, <r> can be comma-separated lists (no whitespace) and can be
  specified many times.  E.g. '-U file1.fq,file2.fq -U file3.fq'.
  可以是多个序列文件用逗号分隔

Options (defaults in parentheses):

 Input:
  -q                 query input files are FASTQ .fq/.fastq (default)
                     输入检索序列为FASTQG格式
  --qseq             query input files are in Illumina's qseq format
                     输入检索序列是Illumina qseq格式
  -f                 query input files are (multi-)FASTA .fa/.mfa
                     输入文件是多个FASTA文件
  -r                 query input files are raw one-sequence-per-line
                     输入检索序列是每行一个原始序列
  -c                 <m1>, <m2>, <r> are sequences themselves, not files
                     直接输入序列，而不是文件
  -s/--skip <int>    skip the first <int> reads/pairs in the input (none)
                     忽略输入序列的前`<int>`个
  -u/--upto <int>    stop after first <int> reads/pairs (no limit)
                     只分析输入序列的前`<int>`个
  -5/--trim5 <int>   trim <int> bases from 5'/left end of reads (0)
                     剪去reads长度为`<int>`的5'端序列
  -3/--trim3 <int>   trim <int> bases from 3'/right end of reads (0)
                     剪去reads长度为`<int>`的3'端序列
  --phred33          qualities are Phred+33 (default)
                     序列质量打分为Phred+33
  --phred64          qualities are Phred+64
                     序列质量打分为Phred+64
  --int-quals        qualities encoded as space-delimited integers
                     序列质量打分为用空格分隔的整数

 Alignment:
  --n-ceil <func>    func for max # non-A/C/G/Ts permitted in aln (L,0,0.15)
                     允许在比对结果中出现的最多非ACTG的计算函数
  --ignore-quals     treat all quality values as 30 on Phred scale (off)
                     将所有质量分值设为30
  --nofw             do not align forward (original) version of read (off)
                     不比对前向的read
  --norc             do not align reverse-complement version of read (off)
                     不比对后向的read

 Spliced Alignment:
  --pen-cansplice <int>              penalty for a canonical splice site (0)
                                     对已知剪接位点的罚分
  --pen-noncansplice <int>           penalty for a non-canonical splice site (12)
                                     对新的剪接位点的罚分
  --pen-canintronlen <func>          penalty for long introns (G,-8,1) with canonical splice sites
                                     对已知剪接位点中长内含子的罚分
  --pen-noncanintronlen <func>       penalty for long introns (G,-8,1) with noncanonical splice sites
                                     对未知剪接位点中长内含子的罚分
  --min-intronlen <int>              minimum intron length (20)
                                     最小允许的内含子长度
  --max-intronlen <int>              maximum intron length (500000)
                                     最大允许的内含子长度
  --known-splicesite-infile <path>   provide a list of known splice sites
                                     提供一个已知的剪接位点列表
  --novel-splicesite-outfile <path>  report a list of splice sites
                                     报告新的剪接位点
  --novel-splicesite-infile <path>   provide a list of novel splice sites
                                     提供新的剪接位点
  --no-temp-splicesite               disable the use of splice sites found
                                     不使用发现的新剪接位点
  --no-spliced-alignment             disable spliced alignment
                                     不允许剪接比对
  --rna-strandness <string>          specify strand-specific information (unstranded)
                                     指定链特异性的信息
  --tmo                              reports only those alignments within known transcriptome
                                     报告只包含已知转录组信息的比对结果
  --dta                              reports alignments tailored for transcript assemblers
                                     结果适合用于stringtie进行转录本的拼接
  --dta-cufflinks                    reports alignments tailored specifically for cufflinks
                                     结果适合于cufflinks的应用
  --avoid-pseudogene                 tries to avoid aligning reads to pseudogenes (experimental option)
                                     避免与假基因的比对
  --no-templatelen-adjustment        disables template length adjustment for RNA-seq reads
                                     不允许对reads的模板长度进行调整

 Scoring:
  --mp <int>,<int>   max and min penalties for mismatch; lower qual = lower penalty <6,2>
                     不匹配的最大与最小罚分值，低质量对应低罚分
  --sp <int>,<int>   max and min penalties for soft-clipping; lower qual = lower penalty <2,1>
                     soft-clipping的最大与最小罚分
  --no-softclip      no soft-clipping
                     不考虑Soft-clipping
  --np <int>         penalty for non-A/C/G/Ts in read/ref (1)
                     对read或参考序列中出现的非ATCG的罚分
  --rdg <int>,<int>  read gap open, extend penalties (5,3)
                     对read的gap-open, gap-extension的罚分
  --rfg <int>,<int>  reference gap open, extend penalties (5,3)
                     对参考序列的gap-open,gap-extension的罚分
  --score-min <func> min acceptable alignment score w/r/t read length
                     (L,0.0,-0.2)
                     相对read长度的最小接受比对分值

 Reporting:
  -k <int> (default: 5) report up to <int> alns per read
                     对每个read只报告`<int>`个比对结果

 Paired-end:
  -I/--minins <int>  minimum fragment length (0), only valid with --no-spliced-alignment
                     paired-end的最小片段长度
  -X/--maxins <int>  maximum fragment length (500), only valid with --no-spliced-alignment
                     最大片段长度
  --fr/--rf/--ff     -1, -2 mates align fw/rev, rev/fw, fw/fw (--fr)
                     `--fr==fw/rev`，`--rf==rev/fw`, `--ff==fw/fw`
  --no-mixed         suppress unpaired alignments for paired reads
                     不输出paired reads的不能匹配的比对结果
  --no-discordant    suppress discordant alignments for paired reads
                     不输出paired-reads的不统一的比对结果

 Output:
  -t/--time          print wall-clock time taken by search phases
                     输出搜索阶段所花费的wall-clock时间
  --un <path>           write unpaired reads that didn't align to <path>
                        输出没有与`<path>`比对的unpaired reads
  --al <path>           write unpaired reads that aligned at least once to <path>
                        输出至少与`<path>`有一次比对的unpaired reads
  --un-conc <path>      write pairs that didn't align concordantly to <path>
  --al-conc <path>      write pairs that aligned concordantly at least once to <path>
  (Note: for --un, --al, --un-conc, or --al-conc, add '-gz' to the option name, e.g.
  --un-gz <path>, to gzip compress output, or add '-bz2' to bzip2 compress output.)
                    将输出结果进行`gz`或者`bz2`压缩
  --summary-file     print alignment summary to this file.
                     将比对的总结输出到文件中
  --new-summary      print alignment summary in a new style, which is more machine-friendly.
                     将比对总结以新的形式输出
  --quiet            print nothing to stderr except serious errors
                     除了严重错误以外，不将任何结果输出到stderr
  --met-file <path>  send metrics to file at <path> (off)
                     将度量值i输出到文件
  --met-stderr       send metrics to stderr (off)
                     将度量值输出到stderr
  --met <int>        report internal counters & metrics every <int> secs (1)
                     每隔`<int>`秒输出当前的内部计数器和度量值
  --no-head          supppress header lines, i.e. lines starting with @
                     不输出header行，也就是所有以`@`开始的行
  --no-sq            supppress @SQ header lines
                     不输出`@SQ`行
  --rg-id <text>     set read group id, reflected in @RG line and RG:Z: opt field
                     设置`@RG`
  --rg <text>        add <text> ("lab:value") to @RG line of SAM header.
                     Note: @RG line only printed when --rg-id is set.
                     将`<text>`加到SAM文件的`@RG`行
  --omit-sec-seq     put '*' in SEQ and QUAL fields for secondary alignments.
                     将"*"置于SEQ和QUAL两列中，进行二次比对

 Performance:
  -o/--offrate <int> override offrate of index; must be >= index's offrate
                     重置索引的`offrate`，该值必须大于原有的`offrate`
  -p/--threads <int> number of alignment threads to launch (1)
                     比对所用的线程数
  --reorder          force SAM output order to match order of input reads
                     强制要求SAM输出顺序比对与输入reads一致
  --mm               use memory-mapped I/O for index; many 'hisat2's can share
                     使用内存映射的I/O作为索引

 Other:
  --qc-filter        filter out reads that are bad according to QSEQ filter
                     根据QSEQ filter过滤输入的reads
  --seed <int>       seed for random number generator (0)
                     设置RNG seeds的值
  --non-deterministic seed rand. gen. arbitrarily instead of using read attributes
                     不根据reads的属性产生随机数
  --remove-chrname   remove 'chr' from reference names in alignment
                     比对结果中的参考序列名称中去除`chr`
  --add-chrname      add 'chr' to reference names in alignment
                     在比对结果的参考序列名称中加入`chr` 
  --version          print version information and quit
                     输出版本信息
  -h/--help          print this usage message
                     输出帮助信息
```
