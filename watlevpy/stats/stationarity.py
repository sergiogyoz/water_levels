def average_smoother(values, continuity_indices=[], m=0, empty_format=None): #average smoother
    """
    returns an array of smoother values using the average of the 2m+1 values center around each value. It makes an average
    of those avaliable if there are missing values. Edge values, or in general more isolated points, are biased being 
    calculated from less values
    """   
    #there's a potential increase of m times the speed if we change the logic of this to work by keeping a 
    #window of 5 and a mask on the valid values an moving it from start to end
    
    if len(continuity_indices)==0:
        #work with values, so holes are in the values in the array as empty_format e.g. -1, None
        newvalues=[None]*len(values);
        for i in range(len(values)):
            s=0; n=0;
            for k in range(-m,m+1):
                try:
                    if values[i+k] != empty_format:
                        s=s+values[i+k];
                        n=n+1;
                except IndexError:
                    pass; #left/right limits
            try:
                newvalues[i]=s/n;
            except (ZeroDivisionError, TypeError):
                newvalues[i]=None; #we could also just pass but... lets not
        return newvalues;
    else:
        if len(values)!=len(continuity_indices) : raise ValueError(f"values and indices are not the same size: {len(values)} and {len(continuity_indices)}");
        newvalues=[0]*len(values);
        #work with indices, so holes are differences of indices values e.g. 1,2,4,...
        for i in range(len(continuity_indices)):
            s=0; n=0;
            for k in range(-m,m+1):
                try:
                    if continuity_indices[i+k]==continuity_indices[i]+k:
                        s=s+values[i+k];
                        n=n+1;
                except IndexError:
                    pass; #left/right limits
            newvalues[i]=s/n;
        return newvalues;
