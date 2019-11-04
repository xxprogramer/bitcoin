// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2019 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

/**
 * Blockchain Pools config
 */
#ifndef BITCOIN_UTIL_POOLS_H
#define BITCOIN_UTIL_POOLS_H

#include <boost/container/flat_map.hpp>
#include <memory>
#include <sync.h>

extern const char * const BITCOIN_POOLS_FILENAME; 

class PoolsConf
{
 public:
    struct PoolNode {
        using PoolMap = boost::container::flat_map<char, std::unique_ptr<PoolNode>>;

        PoolMap nodes;
        std::string name;
    };

    struct PoolsTireTree {
        PoolNode root;
    };
public:
    PoolsConf();

    bool Init();

    bool FindPoolByCoinbase(const std::string& coinbase,std::string& pool_name);

    bool FindPoolByAddr(const std::string& addr,std::string& pool_name);
private:
    bool addTagNode(const std::string& tag,const std::string& name);
private:
    mutable CCriticalSection cs_pools;
    PoolNode m_tag_root GUARDED_BY(cs_pools);
    boost::container::flat_map<std::string,std::string> m_addr_name_map GUARDED_BY(cs_pools);
};

PoolsConf& gPools();

#endif