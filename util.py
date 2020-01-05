import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    huffPickle = pickle.load(tree_stream)
    return huffPickle


    pass

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    huffTree = tree

    # Bits are read and the tree is traversed until a TreeLeaf object is found.
    reachedLeaf = False
    while reachedLeaf == False:
      direction = bitreader.readbit()
      if direction == 0: #goin left
        huffTree =huffTree.getLeft()
        if isinstance(huffTree, huffman.TreeLeaf): # hit a leaf node if true and return val
          reachedLeaf = True
          return huffTree.getValue()
      else:
        huffTree =huffTree.getRight()
        if isinstance(huffTree, huffman.TreeLeaf):
          reachedLeaf = True
          return huffTree.getValue()
    pass


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    decompTree = read_tree(compressed)  # read whole tree

    binary = bitio.BitReader(compressed) # convert compressed to binary
    writing = bitio.BitWriter(uncompressed) # writing to huff tree to var
    end = False
    place = 0 
    while end == False:
    	try:
    		place = decode_byte(decompTree,binary) # compare whole tree with binary
    		writing.writebits(place,8)
    	except:
    		end = True
    writing.flush()
    pass

def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree, tree_stream)
    pass

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    write_tree(tree,compressed)
    table = huffman.make_encoding_table(tree)  # make encoding table from tree
    writing = bitio.BitWriter(compressed)
    for z in uncompressed:
      for asciChar in z:  # go through each asci character in the line and find it on the table which would give the corrosponding binaries
        binary = table [asciChar]
        for singleBit in binary:  # go through each binary and write it, true = 1 false =0
          if singleBit == 1:
            writing.writebit(True)
          elif singleBit == 0:
            writing.writebit(False)
    for singleBit in table[None]:  # table[None] = EOF binary which was not included in the above for loop.
          if singleBit == 1:
            writing.writebit(True)
          elif singleBit == 0:
            writing.writebit(False)
    writing.flush()

